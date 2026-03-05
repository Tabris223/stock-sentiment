# 向量化去重功能实现报告

## 实施时间
2026-03-02

## 验收标准完成情况

- ✅ 创建 vector_dedup.py
- ✅ 修改 News 模型
- ✅ 修改 fetch_news
- ✅ 测试通过

## 详细实现

### 1. 核心模块：`src/analyzer/vector_dedup.py`

**功能**：
- 使用 sentence-transformers 将文本编码为向量
- 支持余弦相似度计算
- 提供重复检测接口

**特性**：
- 延迟加载模型（首次使用时才加载）
- 使用国内镜像：`HF_ENDPOINT=https://hf-mirror.com`
- 模型优先级：
  - Primary: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (稳定)
  - Fallback: `Qwen/Qwen2.5-0.5B-Instruct` (实验性)
- 向量存储格式：pickle 序列化的 numpy 数组
- 单例模式管理全局实例

**主要方法**：
- `encode(text)` - 文本 → 向量（bytes）
- `decode(embedding_bytes)` - bytes → numpy 数组
- `cosine_similarity(vec1, vec2)` - 计算余弦相似度
- `check_duplicate(new_emb, existing_embs, threshold=0.95)` - 检测重复

### 2. 数据库模型：`src/models/news.py`

**修改**：
```python
embedding = Column(LargeBinary, nullable=True)  # 向量嵌入（用于语义去重）
```

**数据库迁移**：
- 已通过 `add_embedding_field.py` 脚本添加字段
- 字段类型：BLOB (SQLite) / LargeBinary (SQLAlchemy)
- 允许为空（兼容历史数据）

### 3. API 集成：`src/api/news.py`

**两级去重流程**：

#### Level 1: 标题哈希去重（已有）
```python
content_hash = calculate_content_hash(title, url)
if db.query(News).filter(News.content_hash == content_hash).first():
    # 跳过重复
```

#### Level 2: 向量语义去重（新增）
```python
# 1. 获取最近 100 条新闻的向量
recent_news = db.query(News.embedding).filter(
    News.embedding.isnot(None)
).order_by(News.created_at.desc()).limit(100).all()

# 2. 编码新新闻（标题 + 头200字）
text = f"{title} {summary[:200]}"
new_embedding = vector_dedup.encode(text)

# 3. 检查相似度
if vector_dedup.check_duplicate(new_embedding, existing_embeddings, threshold=0.95):
    # 跳过重复
```

**性能优化**：
- 只比较最近 100 条新闻（避免全表扫描）
- 向量预加载（批量查询，减少数据库访问）
- 延迟加载模型（减少启动时间）

**统计增强**：
- 新增 `vector_duplicates` 计数
- 详细日志记录

### 4. 测试验证

#### test_simple_dedup.py ✅
- 基本编码功能
- 向量解码功能
- 余弦相似度计算
- 重复检测功能

#### verify_implementation.py ✅
- 文件完整性检查
- 代码集成验证
- 配置正确性验证

## 技术亮点

1. **智能模型选择**：优先使用稳定模型，自动 fallback
2. **性能优化**：限制比较范围为最近 100 条
3. **国内优化**：使用 HuggingFace 镜像加速下载
4. **向后兼容**：embedding 字段允许为空，不影响历史数据
5. **日志完善**：详细记录去重过程和结果

## 使用示例

```python
# 在 fetch_news API 中自动执行
POST /api/news/fetch
{
  "stock_ids": [1, 2, 3],
  "limit": 50
}

# 返回结果包含去重统计
{
  "fetched_count": 100,
  "saved_count": 75,
  "duplicates": 25,
  "message": "Hash去重: 15条, 向量去重: 10条"
}
```

## 注意事项

- ✅ 已配置国内镜像
- ✅ 向量比较只取最近 100 条
- ✅ 未提交 git（按需求）
- ⚠️ 首次使用需要下载模型（约 400MB）

## 后续建议

1. 可以考虑调整阈值（0.95）以适应实际业务需求
2. 可以添加定期清理旧向量的任务
3. 可以监控向量去重的命中率，优化阈值

## 总结

向量化去重功能已完整实现并集成到新闻抓取流程中，实现了：
- 两级去重机制（hash + 语义）
- 高性能实现（限制比较范围）
- 完善的日志和统计
- 所有验收标准通过 ✅
