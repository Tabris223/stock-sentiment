# 情绪仪表盘设计规范

> 版本：v1.0 | 设计师：Iris | 日期：2026-03-03

---

## 1. 设计系统

### 1.1 颜色系统

#### 主色板 - 情绪颜色

| 用途 | 色值 | CSS 变量 | 说明 |
|------|------|----------|------|
| 正面情绪 | `#10B981` | `--color-positive` | 绿色，代表利好 |
| 负面情绪 | `#EF4444` | `--color-negative` | 红色，代表利空 |
| 中性情绪 | `#6B7280` | `--color-neutral` | 灰色，无明显倾向 |

#### 暗色主题背景

| 用途 | 色值 | CSS 变量 | 说明 |
|------|------|----------|------|
| 页面背景 | `#0F172A` | `--bg-primary` | 深蓝黑色 |
| 卡片背景 | `#1E293B` | `--bg-card` | 次深色 |
| 卡片悬浮 | `#334155` | `--bg-card-hover` | 交互态 |
| 分割线 | `#334155` | `--border-color` | 1px 边框 |

#### 文字颜色

| 用途 | 色值 | CSS 变量 | 说明 |
|------|------|----------|------|
| 主标题 | `#F8FAFC` | `--text-primary` | 几乎白色 |
| 次标题 | `#CBD5E1` | `--text-secondary` | 浅灰 |
| 辅助文字 | `#94A3B8` | `--text-tertiary` | 中灰 |
| 禁用文字 | `#64748B` | `--text-disabled` | 深灰 |

#### 状态颜色

| 状态 | 色值 | 说明 |
|------|------|------|
| 警告 | `#F59E0B` | 风险提示背景 |
| 错误 | `#EF4444` | 同负面情绪 |
| 成功 | `#10B981` | 同正面情绪 |
| 信息 | `#3B82F6` | 链接、提示 |

### 1.2 字体系统

```css
/* 字体栈 */
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', Consolas, monospace;

/* 字号规范 */
--font-size-xs: 12px;    /* 辅助信息 */
--font-size-sm: 14px;    /* 次要内容 */
--font-size-base: 16px;  /* 正文 */
--font-size-lg: 18px;    /* 小标题 */
--font-size-xl: 20px;    /* 标题 */
--font-size-2xl: 24px;   /* 大标题 */
--font-size-3xl: 32px;   /* 主标题/数字 */

/* 字重 */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* 行高 */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

### 1.3 间距系统

```css
/* 基础间距单位：4px */
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-5: 20px;
--spacing-6: 24px;
--spacing-8: 32px;
--spacing-10: 40px;
--spacing-12: 48px;
--spacing-16: 64px;

/* 组件内间距 */
--padding-card: 20px;
--padding-section: 24px;

/* 组件外间距 */
--gap-sm: 12px;
--gap-md: 16px;
--gap-lg: 24px;
```

### 1.4 圆角规范

```css
--radius-sm: 4px;    /* 小按钮、标签 */
--radius-md: 8px;    /* 输入框、小组件 */
--radius-lg: 12px;   /* 卡片 */
--radius-xl: 16px;   /* 大卡片 */
--radius-full: 9999px; /* 圆形 */
```

### 1.5 阴影规范

```css
/* 卡片阴影 */
--shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2);

/* 悬浮阴影 */
--shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.4);

/* 强调阴影（负面/风险） */
--shadow-danger: 0 0 20px rgba(239, 68, 68, 0.3);
```

---

## 2. 情绪仪表盘组件

### 2.1 布局结构

```
┌────────────────────────────────────────────────────────────────────┐
│                         情绪仪表盘                                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │   今日情报数量   │  │   负面新闻占比   │  │   平均置信度    │    │
│  │       128       │  │      23.4%      │  │      0.85       │    │
│  │   ↑ 12% vs 昨日  │  │   ⚠️ 需关注     │  │                 │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
│                                                                    │
│  ┌────────────────────────────┐  ┌────────────────────────────┐   │
│  │                            │  │                            │   │
│  │    情绪分布圆环图           │  │      风险提示卡片          │   │
│  │                            │  │                            │   │
│  │      正面 45%              │  │  ⚠️ 检测到 3 条高风险新闻  │   │
│  │      负面 23%              │  │                            │   │
│  │      中性 32%              │  │  • 某公司退市风险          │   │
│  │                            │  │  • 财务造假调查            │   │
│  │       (ECharts 环图)       │  │  • 高管减持公告            │   │
│  │                            │  │                            │   │
│  └────────────────────────────┘  └────────────────────────────┘   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 组件尺寸

#### 统计卡片（Stats Card）

| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 宽度 | 33.33%（自适应） | 100% |
| 高度 | 120px | 100px |
| 内边距 | 20px | 16px |
| 圆角 | 12px | 8px |

```
┌─────────────────────────────┐
│  [Icon]  今日情报数量        │  <- 14px, 次要文字色
│                             │
│         128                 │  <- 32px, 主文字色, Bold
│                             │
│  ↑ 12% vs 昨日              │  <- 12px, 绿色（如为负则红色）
└─────────────────────────────┘
```

#### 情绪分布圆环图（Donut Chart）

| 属性 | 值 |
|------|------|
| 卡片宽度 | 50%（桌面）/ 100%（移动） |
| 图表尺寸 | 240px × 240px |
| 圆环内径 | 60% |
| 边框宽度 | 20px |
| 中心文字 | 情绪总数 |

**ECharts 配置要点**：
```javascript
{
  type: 'pie',
  radius: ['60%', '80%'],  // 圆环
  center: ['50%', '50%'],
  avoidLabelOverlap: false,
  itemStyle: {
    borderRadius: 4,
    borderColor: '#1E293B',
    borderWidth: 2
  },
  label: {
    show: false  // 使用 legend 代替
  }
}
```

#### 风险提示卡片（Risk Alert Card）

| 属性 | 值 |
|------|------|
| 宽度 | 50%（桌面）/ 100%（移动） |
| 内边距 | 24px |
| 背景 | `#1E293B` + 红色边框 1px |
| 最大高度 | 280px（超出滚动） |

```
┌─────────────────────────────────────────┐
│ ⚠️ 检测到 3 条高风险新闻                 │  <- 16px, Bold, 红色
├─────────────────────────────────────────┤
│                                         │
│ 📰 某公司面临退市风险                    │  <- 14px
│    涉及财务造假，投资者需关注            │  <- 12px, 次要文字
│    置信度: 95%                          │  <- 12px
│                                         │
│ 📰 监管部门立案调查                      │
│    涉嫌信息披露违规                      │
│    置信度: 88%                          │
│                                         │
│ 📰 高管减持公告                          │
│    董事长减持 5% 持股                   │
│    置信度: 92%                          │
│                                         │
└─────────────────────────────────────────┘
```

---

## 3. 情绪趋势图组件

### 3.1 布局结构

```
┌────────────────────────────────────────────────────────────────────┐
│                         情绪趋势                                    │
│                    近 7 天情绪变化                                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  [正面 ▇▇]  [负面 ▇▇]  [中性 ▇▇]          <-- 图例                │
│                                                                    │
│  50 ┤                                                             │
│     │        ╭───╮                                                │
│  40 ┤    ╭───╯   ╰───╮        正面                                │
│     │    │           ╰───╮                                       │
│  30 ┤    │               ╰───╮                                   │
│     │╭───╯                   ╰───╮                               │
│  20 ┤╯                           ╰───╮   负面                    │
│     │                                ╰───╮                       │
│  10 ┤                                    ╰───╮                   │
│     │╭──────╮                                ╰───╮   中性        │
│   0 ┼┴──────┴────────────────────────────────────┴────────────   │
│     │ 03/01  03/02  03/03  03/04  03/05  03/06  03/07           │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  悬浮提示:                                                          │
│  ┌─────────────────────────┐                                       │
│  │ 2026-03-03              │                                       │
│  │ 正面: 45  负面: 23  中性: 32│                                    │
│  └─────────────────────────┘                                       │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 组件尺寸

| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 卡片宽度 | 100% | 100% |
| 图表高度 | 320px | 240px |
| 内边距 | 24px | 16px |
| 图例位置 | 顶部 | 底部 |

### 3.3 ECharts 配置

```javascript
{
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1E293B',
    borderColor: '#334155',
    textStyle: { color: '#F8FAFC' },
    formatter: (params) => {
      const date = params[0].axisValue;
      let html = `<div style="font-weight:600;margin-bottom:8px">${date}</div>`;
      params.forEach(p => {
        html += `<div style="display:flex;justify-content:space-between;gap:16px">
          <span>${p.marker} ${p.seriesName}</span>
          <span style="font-weight:600">${p.value}</span>
        </div>`;
      });
      return html;
    }
  },
  legend: {
    data: ['正面', '负面', '中性'],
    top: 0,
    textStyle: { color: '#94A3B8' },
    itemWidth: 12,
    itemHeight: 12,
    itemGap: 24
  },
  grid: {
    left: 40,
    right: 20,
    top: 50,
    bottom: 40
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['03/01', '03/02', '03/03', '03/04', '03/05', '03/06', '03/07'],
    axisLine: { lineStyle: { color: '#334155' } },
    axisLabel: { color: '#94A3B8', fontSize: 12 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#334155', type: 'dashed' } },
    axisLabel: { color: '#94A3B8', fontSize: 12 }
  },
  series: [
    {
      name: '正面',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2, color: '#10B981' },
      itemStyle: { color: '#10B981' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0)' }
          ]
        }
      },
      data: [35, 42, 38, 45, 40, 48, 52]
    },
    {
      name: '负面',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2, color: '#EF4444' },
      itemStyle: { color: '#EF4444' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(239, 68, 68, 0.3)' },
            { offset: 1, color: 'rgba(239, 68, 68, 0)' }
          ]
        }
      },
      data: [18, 22, 15, 20, 25, 19, 16]
    },
    {
      name: '中性',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2, color: '#6B7280' },
      itemStyle: { color: '#6B7280' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(107, 114, 128, 0.2)' },
            { offset: 1, color: 'rgba(107, 114, 128, 0)' }
          ]
        }
      },
      data: [25, 20, 28, 22, 20, 24, 20]
    }
  ]
}
```

---

## 4. 响应式断点

```css
/* 断点定义 */
--breakpoint-sm: 640px;   /* 移动端 */
--breakpoint-md: 768px;   /* 平板 */
--breakpoint-lg: 1024px;  /* 桌面 */
--breakpoint-xl: 1280px;  /* 大屏 */
```

### 4.1 布局适配

| 断点 | 统计卡片 | 圆环图 | 趋势图 | 风险卡片 |
|------|----------|--------|--------|----------|
| < 640px | 1列 | 全宽 | 全宽 | 全宽 |
| 640-1024px | 3列 | 50% | 全宽 | 50% |
| > 1024px | 3列 | 50% | 全宽 | 50% |

---

## 5. 交互动效

### 5.1 卡片悬浮

```css
.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  transition: all 0.2s ease;
}
```

### 5.2 图表动画

- 入场动画：1s，easeOutCubic
- 数据更新：0.5s，easeOutQuart

---

## 6. 无障碍设计

- 颜色对比度：文字 ≥ 4.5:1，大文字 ≥ 3:1
- 不仅依赖颜色：图标 + 颜色组合表示状态
- 键盘可访问：Tab 可聚焦，Enter 可操作
- 屏幕阅读器：aria-label 标注图表含义

---

## 附录：CSS 变量汇总

```css
:root {
  /* 颜色 */
  --color-positive: #10B981;
  --color-negative: #EF4444;
  --color-neutral: #6B7280;
  --bg-primary: #0F172A;
  --bg-card: #1E293B;
  --bg-card-hover: #334155;
  --border-color: #334155;
  --text-primary: #F8FAFC;
  --text-secondary: #CBD5E1;
  --text-tertiary: #94A3B8;
  
  /* 间距 */
  --padding-card: 20px;
  --gap-md: 16px;
  
  /* 圆角 */
  --radius-lg: 12px;
  
  /* 阴影 */
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.4);
}
```

---

*设计规范 v1.0 | Iris | 2026-03-03*
