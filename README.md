# Stock Sentiment

股票舆情监控系统

## 依赖

```bash
pip install feedparser pyyaml
```

## 使用

```bash
# 生成简报
python main.py

# 生成详细报告
python main.py --format full

# 测试模式（48小时）
python main.py --test
```

## 配置

- `config/stocks.yaml` - 监控的股票列表
- `config/feeds.yaml` - RSS 订阅源

## 定时任务

每天早上 8:00 自动推送日报到飞书群。
