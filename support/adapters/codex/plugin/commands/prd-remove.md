# /prd-remove

从当前项目卸载 PRD Helper。

## Workflow

1. 确认用户要卸载
2. 执行卸载脚本，清理 Agent 配置和插件文件
3. 告知用户卸载完成

## 执行

```bash
python3 "{skill_root}/scripts/remove-prd-helper.py" --project . --agent codex
```
