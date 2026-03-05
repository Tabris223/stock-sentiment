# 情绪趋势图设计稿

> 设计师：Iris | 日期：2026-03-03 | 状态：待评审

---

## 设计预览

### 桌面端布局 (1440px)

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────────────┐    ║
║  │                                                                          │    ║
║  │  情绪趋势                              ● 正面  ● 负面  ● 中性             │    ║
║  │  近 7 天情绪变化                                                         │    ║
║  │                                                                          │    ║
║  │  60 ┤                                                                    │    ║
║  │     │                                                                    │    ║
║  │  50 ┤              ╭────╮                                                │    ║
║  │     │          ╭───╯    ╰───╮           ╭───                             │    ║
║  │  40 ┤      ╭───╯              ╰───╮─────╯                                │    ║
║  │     │  ╭───╯                      ╰───╮                                 │    ║
║  │  30 ┤──╯                              ╰───╮                             │    ║
║  │     │                                      ╰───╮                         │    ║
║  │  20 ┤                                          ╰───╮                     │    ║
║  │     │  ╭────╮                                      ╰───╮                 │    ║
║  │  10 ┤──╯    ╰──╮                                       ╰───╮            │    ║
║  │     │           ╰────╮                                      ╰───       │    ║
║  │   0 ┼─────────────────┴────────────────────────────────────────────────   │    ║
║  │     │   03/01   03/02   03/03   03/04   03/05   03/06   03/07            │    ║
║  │                                                                          │    ║
║  └──────────────────────────────────────────────────────────────────────────┘    ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

### 悬浮提示 (Tooltip)

```
┌─────────────────────────────┐
│  📅 2026年03月03日           │  14px, #F8FAFC, Bold
│                             │
│  ● 正面  45 条              │  12px, #10B981
│  ● 负面  23 条              │  12px, #EF4444
│  ● 中性  32 条              │  12px, #6B7280
│  ──────────────────         │
│  合计: 100 条               │  12px, #94A3B8
└─────────────────────────────┘
  背景: #1E293B
  边框: 1px solid #334155
  圆角: 8px
  阴影: 0 4px 12px rgba(0,0,0,0.4)
```

### 趋势卡片组件

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                                                                                │
│  情绪趋势                                          ● 正面  ● 负面  ● 中性      │
│  近 7 天情绪变化                                                               │
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                        │   │
│  │  60 ┤                           ╭────╮                                 │   │
│  │     │                       ╭───╯    ╰───╮                             │   │
│  │  50 ┤                   ╭───╯              ╰───╮                       │   │
│  │     │               ╭───╯                      ╰───╮                   │   │
│  │  40 ┤           ╭───╯                              ╰───╮               │   │
│  │     │       ╭───╯                                      ╰───╮           │   │
│  │  30 ┤   ╭───╯                                              ╰───╮       │   │
│  │     │───╯                                                      ╰───   │   │
│  │  20 ┤                                                            ──╮   │   │
│  │     │                                                              ╰── │   │
│  │  10 ┤                                                                 │   │
│  │     │                                                                 │   │
│  │   0 ┼─────────────────────────────────────────────────────────────────│   │
│  │     │  03/01  03/02  03/03  03/04  03/05  03/06  03/07               │   │
│  │                                                                        │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │  快速筛选:  [7天] [14天] [30天]    股票: [全部 ▼]   类型: [全部 ▼]    │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘

组件尺寸:
- 高度: 400px (含筛选栏)
- 图表区域: 320px
- 筛选栏: 56px
- 内边距: 24px
```

---

## 折线设计细节

### 三条趋势线

| 线条 | 颜色 | 粗细 | 样式 | 面积渐变 |
|------|------|------|------|----------|
| 正面 | #10B981 | 2px | smooth 曲线 | 0.3 → 0 透明 |
| 负面 | #EF4444 | 2px | smooth 曲线 | 0.3 → 0 透明 |
| 中性 | #6B7280 | 2px | smooth 曲线 | 0.2 → 0 透明 |

### 数据点

```
    ╭────●────╮
    │    │    │
    │    │    │
正常态: 6px 圆形，填充色
悬浮态: 10px 圆形，填充色 + 发光
```

### 网格线

```css
/* Y 轴网格 */
splitLine: {
  lineStyle: {
    color: '#334155',
    type: 'dashed',  /* 虚线 */
    width: 1
  }
}

/* X 轴 */
axisLine: {
  lineStyle: {
    color: '#334155',
    type: 'solid',
    width: 1
  }
}
```

---

## 移动端布局 (375px)

```
╔═════════════════════════════╗
║                             ║
║  情绪趋势                   ║
║  近 7 天情绪变化            ║
║                             ║
║  ● 正面 ● 负面 ● 中性       ║
║                             ║
║  ┌───────────────────────┐  ║
║  │  60 ┤                 │  ║
║  │     │    ╭──╮         │  ║
║  │  50 ├───╯  ╰──╮       │  ║
║  │     │         ╰──╮    │  ║
║  │  40 ┤            ╰──  │  ║
║  │     │                 │  ║
║  │  30 ┤                 │  ║
║  │     │                 │  ║
║  │  20 ┤                 │  ║
║  │     │                 │  ║
║  │  10 ┤                 │  ║
║  │   0 ┼────────────────  │  ║
║  │     03/01  03/04  03/07│  ║
║  └───────────────────────┘  ║
║                             ║
║  [7天] [14天] [30天]        ║
║                             ║
╚═════════════════════════════╝

移动端适配:
- 图表高度: 240px (减少 80px)
- X 轴标签: 只显示 3 个日期
- 图例: 移到底部
- 筛选栏: 简化为标签按钮
```

---

## 交互行为

### 1. 数据点悬浮

```
默认态:
    ╭────────╮
    │   ●    │  6px 圆点
    ╰────────╯

悬浮态:
    ╭────────╮
    │   ◉    │  10px 圆点 + 发光效果
    ╰────────╯
    
同时显示 Tooltip:
┌──────────────┐
│ 03/03        │
│ 正面: 45     │
│ 负面: 23     │
│ 中性: 32     │
└──────────────┘
```

### 2. 图例交互

```
● 正面  ● 负面  ● 中性

点击图例:
- 切换该线条的显示/隐藏
- 隐藏时变灰: ● 正面
- 动画: fade 0.3s
```

### 3. 时间范围切换

```
┌──────────────────────────────────────┐
│  [7天]  [14天]  [30天]  [自定义...]   │
│   ↑                                │
│  选中态: bg: #334155, border: #3B82F6│
└──────────────────────────────────────┘

切换动画:
- 旧数据 fadeOut
- 新数据 fadeIn
- 总时长: 0.5s
```

### 4. 缩放/平移（可选）

```javascript
dataZoom: [
  {
    type: 'inside',
    start: 0,
    end: 100
  }
]
// 移动端支持双指缩放
// 桌面端支持滚轮缩放
```

---

## 空状态/异常状态

### 无数据

```
┌────────────────────────────────────┐
│                                    │
│         📊                         │
│     暂无情绪数据                    │
│                                    │
│     请先添加关注股票                │
│     [添加股票 →]                   │
│                                    │
└────────────────────────────────────┘
```

### 加载中

```
┌────────────────────────────────────┐
│                                    │
│  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 50%          │
│                                    │
│      正在加载情绪数据...            │
│                                    │
└────────────────────────────────────┘
```

### 错误状态

```
┌────────────────────────────────────┐
│                                    │
│         ⚠️                         │
│     数据加载失败                    │
│                                    │
│     [点击重试]                     │
│                                    │
└────────────────────────────────────┘
```

---

## ECharts 完整配置

```javascript
const trendChartOption = {
  // 背景透明（使用卡片背景）
  backgroundColor: 'transparent',
  
  // 提示框
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1E293B',
    borderColor: '#334155',
    borderWidth: 1,
    padding: [12, 16],
    textStyle: {
      color: '#F8FAFC',
      fontSize: 12
    },
    formatter: (params) => {
      const date = params[0].axisValue;
      let html = `
        <div style="font-weight:600;margin-bottom:8px;color:#F8FAFC">
          📅 ${date}
        </div>
      `;
      let total = 0;
      params.forEach(p => {
        total += p.value;
        html += `
          <div style="display:flex;justify-content:space-between;gap:24px;margin:4px 0">
            <span>${p.marker} ${p.seriesName}</span>
            <span style="font-weight:600">${p.value} 条</span>
          </div>
        `;
      });
      html += `
        <div style="border-top:1px solid #334155;margin-top:8px;padding-top:8px;
                    display:flex;justify-content:space-between">
          <span style="color:#94A3B8">合计</span>
          <span style="font-weight:600">${total} 条</span>
        </div>
      `;
      return html;
    }
  },
  
  // 图例
  legend: {
    data: ['正面', '负面', '中性'],
    top: 32,
    right: 24,
    textStyle: {
      color: '#94A3B8',
      fontSize: 12
    },
    itemWidth: 12,
    itemHeight: 12,
    itemGap: 16,
    icon: 'circle'
  },
  
  // 标题
  title: {
    text: '情绪趋势',
    subtext: '近 7 天情绪变化',
    left: 24,
    top: 16,
    textStyle: {
      color: '#F8FAFC',
      fontSize: 18,
      fontWeight: 600
    },
    subtextStyle: {
      color: '#94A3B8',
      fontSize: 12
    }
  },
  
  // 网格
  grid: {
    left: 48,
    right: 24,
    top: 80,
    bottom: 48
  },
  
  // X 轴
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['03/01', '03/02', '03/03', '03/04', '03/05', '03/06', '03/07'],
    axisLine: {
      lineStyle: { color: '#334155' }
    },
    axisLabel: {
      color: '#94A3B8',
      fontSize: 12
    },
    axisTick: { show: false }
  },
  
  // Y 轴
  yAxis: {
    type: 'value',
    splitLine: {
      lineStyle: {
        color: '#334155',
        type: 'dashed'
      }
    },
    axisLabel: {
      color: '#94A3B8',
      fontSize: 12
    },
    axisLine: { show: false },
    axisTick: { show: false }
  },
  
  // 系列
  series: [
    {
      name: '正面',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      showSymbol: false,  // 只在悬浮时显示
      lineStyle: {
        width: 2,
        color: '#10B981'
      },
      itemStyle: {
        color: '#10B981',
        borderWidth: 2,
        borderColor: '#1E293B'
      },
      emphasis: {
        scale: true,
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(16, 185, 129, 0.5)'
        }
      },
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
      showSymbol: false,
      lineStyle: {
        width: 2,
        color: '#EF4444'
      },
      itemStyle: {
        color: '#EF4444',
        borderWidth: 2,
        borderColor: '#1E293B'
      },
      emphasis: {
        scale: true,
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(239, 68, 68, 0.5)'
        }
      },
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
      showSymbol: false,
      lineStyle: {
        width: 2,
        color: '#6B7280'
      },
      itemStyle: {
        color: '#6B7280',
        borderWidth: 2,
        borderColor: '#1E293B'
      },
      emphasis: {
        scale: true,
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(107, 114, 128, 0.3)'
        }
      },
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
  ],
  
  // 动画
  animationDuration: 1000,
  animationEasing: 'cubicOut'
};
```

---

## 切图清单

| 名称 | 尺寸 | 格式 | 用途 |
|------|------|------|------|
| icon-calendar.svg | 16×16 | SVG | Tooltip 日期图标 |
| icon-empty-chart.svg | 64×64 | SVG | 空状态图标 |
| icon-error.svg | 64×64 | SVG | 错误状态图标 |

---

*设计稿 v1.0 | Iris | 2026-03-03*
