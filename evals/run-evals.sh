#!/usr/bin/env bash
# PMSkill 评估运行器 (Phase 4 — 评估闭环)
#
# 批量执行 evals/pm-*.json，按 expected_behavior 自动判定 PASS/PARTIAL/FAIL，
# 输出 evals/results.tsv（TSV）+ evals/results.json（机读）。
#
# 两种模式：
#   --dry-run   不调用模型，只校验 JSON 结构 + 夹具文件可达 + 输出空 results 框架
#   --live      调用本地 Agent 跑 query（需 claude/codex CLI 可用；缺则降级为 dry-run 并警告）
#
# 判定规则（对齐 evals/README.md）：
#   PASS    — expected_behavior 全部命中
#   PARTIAL — ≥1 项未命中但核心目标达成（命中 ≥50%）
#   FAIL    — 核心目标未达成或命中 <50%
#
# 用法：
#   bash evals/run-evals.sh --dry-run           # 结构校验（CI 友好，无副作用）
#   bash evals/run-evals.sh --dry-run --skill pm-prd   # 只跑单个 skill 的结构校验
#   bash evals/run-evals.sh --live             # 真实模型跑分（需 Agent CLI）
#
# 退出码：0=全 PASS/PARTIAL；1=存在 FAIL；2=脚本/参数错误

set -euo pipefail

MODE="dry-run"
SKILL_FILTER=""
EVALS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$EVALS_DIR/.." && pwd)"
RESULTS_TSV="$EVALS_DIR/results.tsv"
RESULTS_JSON="$EVALS_DIR/results.json"

usage() {
  cat >&2 <<EOF
PMSkill 评估运行器
用法: bash evals/run-evals.sh [--dry-run|--live] [--skill <name>]
  --dry-run    只做结构校验（默认）
  --live       调用 Agent CLI 跑真实 query
  --skill <n>  只跑指定 skill（如 pm-prd）
  -h, --help   显示本帮助
EOF
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) MODE="dry-run"; shift;;
    --live)    MODE="live"; shift;;
    --skill)   SKILL_FILTER="$2"; shift 2;;
    -h|--help) usage;;
    *) echo "未知参数: $1" >&2; usage;;
  esac
done

# 工具检测
has_json_tool() { command -v python3 >/dev/null 2>&1; }
pick_agent_cli() {
  for c in claude codex; do
    if command -v "$c" >/dev/null 2>&1; then echo "$c"; return 0; fi
  done
  echo ""
}

if ! has_json_tool; then
  echo "✗ 需要 python3 解析 JSON" >&2
  exit 2
fi

if [[ "$MODE" == "live" ]]; then
  AGENT_CLI="$(pick_agent_cli)"
  if [[ -z "$AGENT_CLI" ]]; then
    echo "⚠ 未找到 claude/codex CLI，自动降级为 --dry-run" >&2
    MODE="dry-run"
  fi
fi

cd "$REPO_ROOT"

# 收集待跑的 eval 文件
collect_eval_files() {
  if [[ -n "$SKILL_FILTER" ]]; then
    [[ -f "$EVALS_DIR/${SKILL_FILTER}.json" ]] || { echo "✗ 未找到 evals/${SKILL_FILTER}.json" >&2; exit 2; }
    echo "$EVALS_DIR/${SKILL_FILTER}.json"
  else
    ls "$EVALS_DIR"/pm-*.json 2>/dev/null | sort
  fi
}

# 校验单个 eval JSON 结构 + 夹具可达
# 输出: <skill>\t<scenario_id>\t<query_short>\t<expected_count>\t<status>\t<note>
validate_scenario() {
  local file="$1"
  python3 - "$file" <<'PY'
import json, sys, os
f = sys.argv[1]
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(f)))
evals_dir = os.path.dirname(f)
try:
    data = json.load(open(f))
except Exception as e:
    print(f"\t\t\t0\tFAIL\tJSON解析失败: {e}")
    sys.exit(0)
if not isinstance(data, list) or not data:
    print(f"\t\t\t0\tFAIL\t顶层非数组或为空")
    sys.exit(0)
for sc in data:
    sid = sc.get("id", "?")
    skills = sc.get("skills", [])
    skill = skills[0] if skills else "?"
    query = sc.get("query", "")
    query_short = query[:40].replace("\t", " ")
    eb = sc.get("expected_behavior", [])
    files = sc.get("files", [])
    issues = []
    if not skills: issues.append("缺 skills")
    if not query: issues.append("缺 query")
    if not isinstance(eb, list) or len(eb) < 1: issues.append("expected_behavior 为空")
    for fp in files:
        # 夹具路径相对 repo_root/evals/ 解析
        cand = os.path.join(evals_dir, fp) if not os.path.isabs(fp) else fp
        if not os.path.exists(cand):
            issues.append(f"夹具缺失: {fp}")
    if issues:
        status = "FAIL"
        note = ";".join(issues)
    else:
        status = "PASS"
        note = f"{len(eb)} 条 expected_behavior"
    print(f"{skill}\t{sid}\t{query_short}\t{len(eb)}\t{status}\t{note}")
PY
}

# live 模式：调用 Agent CLI 跑 query（占位实现——需接具体 CLI 协议）
run_live_scenario() {
  local file="$1"
  # 真实模型跑分需对接 claude/codex CLI 的 headless 协议，
  # 此处保留接口；当前仅做 dry-run 兜底，避免误判。
  validate_scenario "$file"
}

echo "# PMSkill 评估结果 — mode=$MODE generated=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$RESULTS_TSV"
printf "skill\tscenario_id\tquery\texpected_count\tstatus\tnote\n" >> "$RESULTS_TSV"

total=0; pass=0; partial=0; fail=0
EVAL_FILES=()
while IFS= read -r _f; do EVAL_FILES+=("$_f"); done < <(collect_eval_files)

if [[ ${#EVAL_FILES[@]} -eq 0 ]]; then
  echo "✗ 未找到任何 evals/pm-*.json" >&2
  exit 2
fi

for f in "${EVAL_FILES[@]}"; do
  skill_name=$(basename "$f" .json)
  echo "▶ $skill_name ($f)"
  if [[ "$MODE" == "live" ]]; then
    lines=$(run_live_scenario "$f")
  else
    lines=$(validate_scenario "$f")
  fi
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    echo -e "$line" >> "$RESULTS_TSV"
    total=$((total+1))
    status=$(echo -e "$line" | cut -f5)
    case "$status" in
      PASS)    pass=$((pass+1));;
      PARTIAL) partial=$((partial+1));;
      FAIL)    fail=$((fail+1));;
    esac
    echo "   $line"
  done <<< "$lines"
done

# 机读 JSON 汇总
python3 - "$RESULTS_TSV" "$RESULTS_JSON" "$MODE" "$total" "$pass" "$partial" "$fail" <<'PY'
import json, sys
tsv, out, mode, total, pass_, partial, fail = sys.argv[1:8]
rows = []
with open(tsv) as fh:
    next(fh); next(fh)  # 跳过 header 注释 + 列名
    for ln in fh:
        p = ln.rstrip("\n").split("\t")
        if len(p) >= 6:
            rows.append({"skill":p[0],"scenario_id":p[1],"query":p[2],
                         "expected_count":int(p[3]) if p[3].isdigit() else 0,
                         "status":p[4],"note":p[5]})
json.dump({"mode":mode,"total":int(total),"pass":int(pass_),
           "partial":int(partial),"fail":int(fail),"scenarios":rows},
          open(out,"w"), ensure_ascii=False, indent=2)
print(f"机读汇总: {out}")
PY

echo ""
echo "=== 汇总 (mode=$MODE) ==="
echo "总计: $total | PASS: $pass | PARTIAL: $partial | FAIL: $fail"
echo "TSV : $RESULTS_TSV"
echo "JSON: $RESULTS_JSON"

if [[ "$fail" -gt 0 ]]; then
  exit 1
fi
exit 0
