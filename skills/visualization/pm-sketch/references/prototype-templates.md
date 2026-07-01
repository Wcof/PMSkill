# HTML 原型模板集

> 由 `/pm-sketch --prototype` 根据技术栈决策结果选用的 HTML 模板。详见 `SKILL.md` 的「Step 0：技术栈决策」和「HTML 原型」节。

## Vue3 CDN 模板

当检测到 Vue3 或新项目推荐 Vue3 时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语，使用 Vue 的 class/style 绑定 */
  </style>
</head>
<body>
  <div id="app">
    <nav>
      <a v-for="page in pages" :key="page.id" :href="'#' + page.id">{{ page.name }}</a>
    </nav>
    <section v-for="page in pages" :key="page.id" :id="page.id">
      <h1>{{ page.title }}</h1>
    </section>
  </div>
  <script>
    const { createApp, ref, computed } = Vue
    const app = createApp({
      setup() {
        const pages = ref([/* 从 PMContext 提取的页面数据 */])
        return { pages }
      }
    })
    app.mount('#app')
  </script>
</body>
</html>
```

## React CDN 模板

当检测到 React 或新项目推荐 React 时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语 */
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect } = React
    const pages = [/* 从 PMContext 提取的页面数据 */]

    const App = () => (
      <>
        <nav>
          {pages.map(p => <a key={p.id} href={'#'+p.id}>{p.name}</a>)}
        </nav>
        {pages.map(p => (
          <section key={p.id} id={p.id}>
            <h1>{p.title}</h1>
          </section>
        ))}
      </>
    )

    ReactDOM.createRoot(document.getElementById('root')).render(<App />)
  </script>
</body>
</html>
```

## Plain HTML 兜底模板

当检测到 Angular / 无框架 / 技术栈冲突或 CDN 不可达时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语 */
  </style>
</head>
<body>
  <nav>
    <a href="#page1">页面1</a>
    <a href="#page2">页面2</a>
  </nav>
  <section id="page1">
    <h1>页面1: <名称></h1>
  </section>
  <section id="page2">
    <h1>页面2: <名称></h1>
  </section>
  <script>
    // 交互：页面切换、表单验证、状态切换（可选）
  </script>
</body>
</html>
```

## 适配标注片段

### Electron 标注

当检测到或推荐 Electron 时，在原型顶部添加：

```html
<!-- 🖥 此原型推荐用 Electron 包装运行。Electron 主进程配置见 electron/main.js -->
```

### 移动端适配

当检测到或推荐 Flutter / React Native 时，HTML 原型不适用，输出 `design-spec.md` 替代，包含屏幕设计说明 + 组件规范 + 交互描述。

## 质量清单

生成后逐项检查：
- ✅ 技术栈决策有依据（新项目推荐 / 老项目扫描检测 `package.json` 等）
- ✅ 使用推荐/检测到的技术栈 CDN 版本（Vue3 / React / Plain HTML 兜底）
- ✅ 响应式设计（移动端 ≤ 640px / 桌面端 ≥ 1024px 两套布局）
- ✅ 所有页面/组件都对应 PMContext 中的实体/关系
- ✅ 无法对应 PMContext 的图元标 `[假设]` 注释
- ✅ 交互可操作（点击/切换/表单输入等 demo 级别即可）
- ✅ UTF-8 编码，中文字符正常显示
- ✅ 原型文件 `prototype.html` < 200KB（不含 CDN 外部资源体积）
- ✅ Electron 或移动端适配标注已添加