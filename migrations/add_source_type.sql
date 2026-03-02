-- 添加 source_type 字段到 news 表
-- 执行前请备份数据库

-- 方案1：简单添加列（SQLite 支持）
ALTER TABLE news ADD COLUMN source_type VARCHAR(20) DEFAULT 'stock_news';
CREATE INDEX IF NOT EXISTS idx_news_source_type ON news(source_type);

-- 方案2：完整重建表（如果需要修改 stock_id 为可空）
-- 取消下面的注释执行
/*
BEGIN TRANSACTION;

CREATE TABLE news_new (
    id INTEGER PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),  -- 改为可空
    title VARCHAR(500) NOT NULL,
    content TEXT,
    source VARCHAR(100),
    source_type VARCHAR(20) DEFAULT 'stock_news',
    publish_time TIMESTAMP,
    url VARCHAR(1000),
    content_hash VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO news_new 
SELECT id, stock_id, title, content, source, 'stock_news', publish_time, url, content_hash, created_at 
FROM news;

DROP TABLE news;
ALTER TABLE news_new RENAME TO news;

-- 重建索引
CREATE INDEX idx_news_stock_id ON news(stock_id);
CREATE INDEX idx_news_source_type ON news(source_type);
CREATE INDEX idx_news_publish_time ON news(publish_time);
CREATE INDEX idx_news_content_hash ON news(content_hash);

COMMIT;
*/
