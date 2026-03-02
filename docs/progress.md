# Stock Sentiment 项目进度

**最后更新**：2026-03-02 10:12

---

## ✅ P1.1 股票注册 API - 已完成

**Issue**：#1  
**Commit**：cee4981  
**状态**：已发布

**API 端点**：
- POST /api/v1/stocks
- GET /api/v1/stocks
- DELETE /api/v1/stocks/{id}

---

## 🔄 P1.2 新闻抓取模块 - 修复完成，待复审

**Issue**：#2  
**状态**：后端修复完成，待架构师复审

### 进度

| 阶段 | 状态 |
|:----:|:----:|
| @backend-dev 开发 | ✅ |
| @architect 审核 | ✅ 发现 4 个问题 |
| @backend-dev 修复 | ✅ |
| 复合索引添加 | ✅ |
| @architect 复审 | ⏳ |
| @cto 审核 | ⏳ |
| @qa 测试 | ⏳ |
| @product 验收 | ⏳ |

### 修复记录

| # | 问题 | 严重度 | 状态 |
|:-:|------|:------:|:----:|
| 1 | 时间解析未实现 | 中 | ✅ 已修复 |
| 2 | 错误用 print 而非 logger | 中 | ✅ 确认无问题 |
| 3 | 缺少复合索引 `idx_stock_publish` | 低 | ✅ 已添加 |
| 4 | 路由歧义 `/news/{stock_id}` | 低 | ✅ 确认无问题 |

### 修复详情

**1. 时间解析（已修复）**
- 文件：`src/fetcher/multi_source_fetcher.py`
- 添加 `_parse_publish_time()` 方法
- 所有数据源改用该方法解析时间字段

**2. print/logger（确认无问题）**
- 代码已使用 logging 模块
- 仅测试脚本使用 print

**3. 复合索引（已添加）**
- 索引：`idx_stock_publish ON news(stock_id, publish_time)`
- 时间：2026-03-02 04:34

**4. 路由歧义（确认无问题）**
- 实际路由是 `/news/stock/{stock_id}`
- 不会与未来 `/news/meta/sources` 冲突

---

## ✅ 数据源扩展 - 已完成

**状态**：开发完成，测试通过

### 新增数据源

| 数据源 | 函数 | 状态 |
|--------|------|:----:|
| 个股新闻 | stock_news_em | ✅ |
| 财经新闻 | stock_news_main_cx | ✅ |
| 央视新闻 | news_cctv | ✅ |
| 研报 | stock_research_report_em | ✅ |
| 个股资金流 | stock_individual_fund_flow | ✅ |
| 行业资金流 | stock_sector_fund_flow_rank | ⚠️ 限流 |

### 新增文件

- `src/fetcher/multi_source_fetcher.py` - 多数据源抓取器
- `migrations/add_source_type.sql` - 数据库迁移
- `docs/multi_source_usage.md` - 使用说明

### 修改文件

- `src/models/news.py` - 添加 source_type 字段
- `src/schemas/news.py` - 添加 sources 参数
- `src/api/news.py` - 支持多数据源

---

## 当前节点

**时间**：2026-03-02 10:12  
**状态**：Gateway 更新前，代码已提交  
**下一步**：架构师复审 → CTO 审核 → QA 测试 → 产品验收

---

## GitHub

- 仓库：https://github.com/Tabris223/stock-sentiment
- 看板：https://github.com/users/Tabris223/projects/4
