# 多数据源新闻抓取器使用说明

## 📋 概述

已扩展系统支持 5 个数据源，按优先级分类：

### P0（必须）
1. **stock_news_em** - 东财个股新闻（原有）
2. **stock_news_main_cx** - 东财财经新闻（100条综合新闻）✅
3. **news_cctv** - 央视新闻（权威来源）✅

### P1（重要）
4. **stock_research_report_em** - 研报摘要 ✅
5. **stock_sector_fund_flow_rank** - 行业资金流 ⚠️（偶发性网络问题）
6. **stock_individual_fund_flow** - 个股资金流 ✅

## 🗂️ 创建的文件

1. **src/fetcher/multi_source_fetcher.py** - 统一多数据源抓取器
2. **migrations/add_source_type.sql** - 数据库迁移脚本

## 📝 修改的文件

1. **src/models/news.py** - 添加 `source_type` 字段和 `SourceType` 枚举
2. **src/schemas/news.py** - 添加 `SourceType` 枚举和 `source_stats` 字段
3. **src/api/news.py** - 更新 API 支持多数据源参数

## 🚀 快速开始

### 1. 数据库迁移

```bash
# 进入项目目录
cd /Users/damin1206/.openclaw/workspace/stock-sentiment

# 执行迁移（SQLite）
sqlite3 data/stock_sentiment.db < migrations/add_source_type.sql
```

### 2. 启动服务

```bash
uvicorn app:app --reload
```

### 3. API 使用

#### 抓取所有数据源（默认）

```bash
curl -X POST http://localhost:8000/api/v1/news/fetch \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 指定数据源

```bash
curl -X POST http://localhost:8000/api/v1/news/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["stock_news", "finance_news", "cctv_news"],
    "limit": 20
  }'
```

#### 抓取指定股票的新闻

```bash
curl -X POST http://localhost:8000/api/v1/news/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "stock_ids": [1, 2, 3],
    "sources": ["stock_news", "fund_flow"],
    "limit": 50
  }'
```

#### 按来源类型查询新闻

```bash
# 查询所有财经新闻
curl "http://localhost:8000/api/v1/news?source_type=finance_news&limit=20"

# 查询所有研报
curl "http://localhost:8000/api/v1/news?source_type=research&limit=20"
```

## 📊 响应示例

```json
{
  "fetched_count": 156,
  "saved_count": 142,
  "duplicates": 14,
  "source_stats": {
    "stock_news": {"fetched": 50, "saved": 45, "duplicates": 5},
    "finance_news": {"fetched": 100, "saved": 95, "duplicates": 5},
    "cctv_news": {"fetched": 5, "saved": 2, "duplicates": 3},
    "research": {"fetched": 1, "saved": 0, "duplicates": 1}
  },
  "message": "成功抓取 156 条数据，保存 142 条新记录，跳过 14 条重复"
}
```

## 🔧 数据源类型说明

| source_type | 说明 | 示例来源 |
|------------|------|---------|
| `stock_news` | 个股新闻 | 东方财富个股新闻 |
| `finance_news` | 财经新闻 | 东方财富综合财经新闻 |
| `cctv_news` | 央视新闻 | 央视财经频道 |
| `research` | 研报摘要 | 券商研究报告 |
| `fund_flow` | 资金流 | 行业/个股资金流向 |

## ⚠️ 已知问题

1. **行业资金流（stock_sector_fund_flow_rank）** - 偶发性连接失败
   - 原因：东方财富服务器限流或网络不稳定
   - 解决：已实现自动容错，不影响其他数据源抓取

2. **央视新闻** - 抓取速度较慢
   - 原因：需要爬取多个页面
   - 影响：首次抓取可能需要 1-2 秒

## 🧪 测试

运行测试脚本：

```bash
python3 src/fetcher/multi_source_fetcher.py
```

测试结果（2026-03-02）：
- ✅ 个股新闻 - 5/5 条
- ✅ 财经新闻 - 5/5 条  
- ✅ 央视新闻 - 5/5 条
- ✅ 研报 - 5/5 条
- ⚠️ 行业资金流 - 0/5 条（网络问题）
- ✅ 个股资金流 - 1/1 条

## 📚 代码示例

### Python 直接使用

```python
from src.fetcher.multi_source_fetcher import MultiSourceFetcher

# 初始化抓取器
fetcher = MultiSourceFetcher()

# 抓取所有数据源
entries = fetcher.fetch_all(limit=20)

# 只抓取财经新闻和央视新闻
fetcher = MultiSourceFetcher(enabled_sources=["finance_news", "cctv_news"])
entries = fetcher.fetch_all(limit=20)

# 抓取指定股票的个股新闻和资金流
stocks = [{"code": "601872", "name": "招商轮船"}]
entries = fetcher.fetch_all(
    sources=["stock_news", "fund_flow"],
    stocks=stocks,
    limit=50
)

# 打印结果
for entry in entries[:10]:
    print(f"[{entry['source_type']}] {entry['title']}")
```

## 🔄 后续优化建议

1. **添加重试机制** - 对失败的数据源自动重试 3 次
2. **异步抓取** - 使用 asyncio 并发抓取多个数据源
3. **缓存优化** - 对研报等低频更新数据源添加缓存
4. **监控告警** - 当某个数据源连续失败时发送告警

---

**创建时间**: 2026-03-02  
**作者**: Linus (Backend Dev)
