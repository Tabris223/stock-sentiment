# 情绪分析输出格式规范

> 本文档定义 Stock Sentiment 系统的情绪分析输出格式，供后端（Linus）和前端（Dan）参考。

## 版本信息

- **版本**：v1.0
- **更新日期**：2024年
- **维护团队**：Stock Sentiment Team

---

## 1. 输出结构

### 1.1 完整输出示例

```json
{
  "sentiment": "positive",
  "confidence": 0.85,
  "summary": "一句话总结新闻核心内容和情绪倾向",
  "key_points": [
    "关键点1：具体事实或数据",
    "关键点2：主要影响",
    "关键点3：其他重要信息"
  ],
  "risk_alert": "风险提示内容，如无则为 null",
  "confidence_reason": "置信度评估依据简述"
}
```

### 1.2 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sentiment` | string | ✓ | 情绪分类：`positive` / `negative` / `neutral` |
| `confidence` | number | ✓ | 置信度，范围 0-1，保留2位小数 |
| `summary` | string | ✓ | 一句话摘要，不超过50字 |
| `key_points` | array | ✓ | 关键点列表，3-5条，每条不超过30字 |
| `risk_alert` | string/null | ✓ | 风险提示，无风险时为 `null` |
| `confidence_reason` | string | ○ | 置信度评估依据（可选，调试用） |

---

## 2. 枚举值定义

### 2.1 sentiment（情绪分类）

| 值 | 中文 | 说明 | 典型场景 |
|----|------|------|----------|
| `positive` | 正面 | 利好消息，可能推动股价上涨 | 业绩增长、获得订单、政策利好、产品创新 |
| `negative` | 负面 | 利空消息，可能导致股价下跌 | 业绩下滑、违规处罚、高管风险、退市风险 |
| `neutral` | 中性 | 无明显利好或利空 | 符合预期的公告、常规运营数据、政策维持 |

### 2.2 confidence（置信度）分级

| 区间 | 等级 | 含义 | 建议处理方式 |
|------|------|------|--------------|
| 0.9-1.0 | 极高 | 情绪极其明确，有确凿数据支撑 | 可作为重要决策参考 |
| 0.8-0.9 | 高 | 情绪清晰，有明显事实依据 | 可作为一般决策参考 |
| 0.7-0.8 | 较高 | 情绪较为明确，有一定依据 | 可参考，需结合其他信息 |
| 0.6-0.7 | 中等 | 情绪倾向存在，但存在不确定性 | 谨慎参考 |
| 0.5-0.6 | 较低 | 情绪模糊，难以判断 | 不建议作为主要参考 |
| < 0.5 | 低 | 信息不足或高度矛盾 | 建议忽略或人工审核 |

---

## 3. 数据类型规范

### 3.1 confidence

```typescript
// TypeScript 类型定义
type Confidence = number; // 0 <= x <= 1

// 示例值
const validValues = [0.95, 0.85, 0.72, 0.65, 0.55];
const invalidValues = [-0.1, 1.5, "0.8", null];
```

**后端处理建议**：
- 存储：使用 `DECIMAL(3,2)` 或 `FLOAT`
- 校验：确保值在 [0, 1] 范围内
- 默认值：无（必须由 LLM 返回）

### 3.2 key_points

```typescript
// TypeScript 类型定义
type KeyPoints = string[]; // 3-5 条

// 校验规则
const rules = {
  minLength: 3,
  maxLength: 5,
  itemMaxLength: 30 // 每条不超过30字
};

// 示例
const validKeyPoints = [
  "营收1505.6亿元，同比增长18.2%",
  "净利润757.5亿元，同比增长15.3%",
  "茅台酒毛利率稳定在92%以上"
];
```

**后端处理建议**：
- 存储：可使用 JSON 类型或拆分为关联表
- 前端展示：建议使用列表/标签形式

### 3.3 summary

```typescript
// TypeScript 类型定义
type Summary = string; // 不超过50字

// 校验规则
const rules = {
  maxLength: 50
};
```

**前端展示建议**：
- 作为主要摘要文本展示
- 可配合情绪颜色标签使用

### 3.4 risk_alert

```typescript
// TypeScript 类型定义
type RiskAlert = string | null;

// 示例
const withRisk = {
  "risk_alert": "涉及退市风险，投资者需关注维权进展"
};

const withoutRisk = {
  "risk_alert": null
};
```

**前端展示建议**：
- 仅当值不为 `null` 时显示风险提示
- 建议使用警告样式（如红色/橙色标签）

---

## 4. API 接口规范

### 4.1 请求格式

```http
POST /api/v1/sentiment/analyze
Content-Type: application/json

{
  "news": [
    {
      "id": "news_001",
      "title": "贵州茅台年报净利润增长15.3%",
      "summary": "贵州茅台发布2024年年报..."
    }
  ],
  "options": {
    "includeConfidenceReason": true,
    "maxKeyPoints": 5
  }
}
```

### 4.2 响应格式

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": 0,
  "message": "success",
  "data": {
    "results": [
      {
        "id": "news_001",
        "sentiment": "positive",
        "confidence": 0.92,
        "summary": "茅台2024年报业绩亮眼",
        "key_points": [
          "营收1505.6亿元，同比增长18.2%",
          "净利润757.5亿元，同比增长15.3%"
        ],
        "risk_alert": null,
        "confidence_reason": "业绩数据明确..."
      }
    ],
    "stats": {
      "total": 1,
      "positive": 1,
      "negative": 0,
      "neutral": 0,
      "avgConfidence": 0.92
    }
  }
}
```

### 4.3 错误响应

```json
{
  "code": 400,
  "message": "Invalid input: title is required",
  "data": null
}
```

---

## 5. 前端展示建议

### 5.1 情绪颜色映射

```css
/* 推荐配色方案 */
.sentiment-positive { color: #52c41a; } /* 绿色 */
.sentiment-negative { color: #ff4d4f; } /* 红色 */
.sentiment-neutral  { color: #8c8c8c; } /* 灰色 */

/* 置信度颜色（可选） */
.confidence-high    { color: #1890ff; } /* 蓝色，>0.8 */
.confidence-medium  { color: #faad14; } /* 橙色，0.6-0.8 */
.confidence-low     { color: #ff4d4f; } /* 红色，<0.6 */
```

### 5.2 UI 组件建议

```
┌─────────────────────────────────────────────────┐
│ [正面] 茅台2024年报业绩亮眼          置信度: 92% │
├─────────────────────────────────────────────────┤
│ • 营收1505.6亿元，同比增长18.2%                  │
│ • 净利润757.5亿元，同比增长15.3%                 │
│ • 茅台酒毛利率稳定在92%以上                      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ [负面] ⚠️ 退市风险                     置信度: 95% │
├─────────────────────────────────────────────────┤
│ 风险提示: 涉及退市风险，投资者需关注维权进展      │
│ • 公司连续多年财务造假                           │
│ • 已被交易所作出强制退市决定                     │
│ • 约10万投资者面临损失                          │
└─────────────────────────────────────────────────┘
```

### 5.3 图表展示建议

- **情绪分布饼图**：显示 positive/negative/neutral 的占比
- **置信度分布图**：按置信度区间统计新闻数量
- **时间趋势图**：情绪随时间的变化趋势

---

## 6. 数据存储建议

### 6.1 数据库表结构（参考）

```sql
CREATE TABLE sentiment_results (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  news_id VARCHAR(64) NOT NULL,
  news_title VARCHAR(255) NOT NULL,
  news_summary TEXT,
  sentiment ENUM('positive', 'negative', 'neutral') NOT NULL,
  confidence DECIMAL(3,2) NOT NULL,
  summary VARCHAR(100) NOT NULL,
  key_points JSON,
  risk_alert TEXT,
  confidence_reason VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_news_id (news_id),
  INDEX idx_sentiment (sentiment),
  INDEX idx_confidence (confidence)
);
```

### 6.2 缓存策略

- 相同新闻（标题+摘要哈希）的分析结果可缓存
- 建议缓存时间：24-48小时
- 缓存键：`sentiment:{hash(news_title + news_summary)}`

---

## 7. 异常情况处理

### 7.1 LLM 返回格式异常

```javascript
// 后端解析异常处理
function parseSentimentResponse(rawResponse) {
  try {
    const parsed = JSON.parse(rawResponse);
    
    // 校验必填字段
    if (!parsed.sentiment || !parsed.confidence || !parsed.summary) {
      throw new Error('Missing required fields');
    }
    
    // 校验枚举值
    if (!['positive', 'negative', 'neutral'].includes(parsed.sentiment)) {
      throw new Error('Invalid sentiment value');
    }
    
    // 校验置信度范围
    if (parsed.confidence < 0 || parsed.confidence > 1) {
      throw new Error('Confidence out of range');
    }
    
    return parsed;
  } catch (e) {
    // 返回默认值或标记为需要人工审核
    return {
      sentiment: 'neutral',
      confidence: 0.5,
      summary: '解析失败，需人工审核',
      key_points: [],
      risk_alert: null,
      _parseError: true
    };
  }
}
```

### 7.2 边界情况

| 情况 | 处理建议 |
|------|----------|
| 标题或摘要为空 | 返回错误，不进行分析 |
| 标题过长（>200字） | 截断后分析，降低置信度 |
| 摘要过长（>1000字） | 截断或分段分析 |
| 非中文内容 | 提示不支持或使用翻译后分析 |
| 包含敏感词 | 正常分析，存储时脱敏处理 |

---

## 8. 版本兼容

### 8.1 字段扩展

新增字段时遵循以下规则：
- 新增可选字段：向后兼容
- 新增必填字段：需要版本升级
- 删除字段：保留一个版本的过渡期，标记为 deprecated

### 8.2 版本号规则

- 主版本号：不兼容的 API 变更
- 次版本号：向后兼容的功能新增
- 修订号：向后兼容的问题修复

---

## 附录：完整示例

### A. 批量分析请求

```json
{
  "news": [
    {
      "id": "n001",
      "title": "贵州茅台年报净利润增长15.3%",
      "summary": "贵州茅台发布2024年年报..."
    },
    {
      "id": "n002",
      "title": "某公司财务造假被强制退市",
      "summary": "某A股上市公司因连续多年..."
    },
    {
      "id": "n003",
      "title": "央行维持LPR不变",
      "summary": "中国人民银行公布最新LPR报价..."
    }
  ]
}
```

### B. 批量分析响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "results": [
      {
        "id": "n001",
        "sentiment": "positive",
        "confidence": 0.92,
        "summary": "茅台2024年报业绩亮眼",
        "key_points": ["营收增长18.2%", "净利润增长15.3%"],
        "risk_alert": null
      },
      {
        "id": "n002",
        "sentiment": "negative",
        "confidence": 0.95,
        "summary": "某公司因财务造假被强制退市",
        "key_points": ["连续多年财务造假", "10万投资者面临损失"],
        "risk_alert": "涉及退市风险"
      },
      {
        "id": "n003",
        "sentiment": "neutral",
        "confidence": 0.88,
        "summary": "LPR维持不变符合预期",
        "key_points": ["1年期和5年期LPR均维持不变"],
        "risk_alert": null
      }
    ],
    "stats": {
      "total": 3,
      "positive": 1,
      "negative": 1,
      "neutral": 1,
      "avgConfidence": 0.92
    }
  }
}
```

---

*文档结束 | 如有问题请联系 Stock Sentiment Team*
