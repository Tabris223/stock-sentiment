#!/usr/bin/env python3
"""Stock Sentiment - 股票舆情监控系统

主入口
"""
import sys
import yaml
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fetcher.akshare_fetcher import AkShareNewsFetcher
from analyzer.sentiment_analyzer import SentimentAnalyzer
from reporter.daily_reporter import DailyReporter


def load_stocks_config() -> list:
    """加载股票配置"""
    config_path = Path(__file__).parent / "config" / "stocks.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config.get('stocks', [])


def run_daily_report(hours: int = 24, output_format: str = "brief") -> str:
    """运行日报生成
    
    Args:
        hours: 统计时间范围（小时）
        output_format: 输出格式，"brief" 或 "full"
    
    Returns:
        日报文本
    """
    print(f"🔍 开始抓取舆情数据...")
    
    # 加载股票配置
    stocks = load_stocks_config()
    print(f"  监控股票: {[s['name'] for s in stocks]}")
    
    # 1. 抓取新闻
    fetcher = AkShareNewsFetcher()
    all_entries = fetcher.fetch_all(stocks)
    print(f"  共抓取 {len(all_entries)} 条新闻")
    
    if not all_entries:
        print("  ⚠️ 无相关舆情信息")
        reporter = DailyReporter()
        return reporter.generate_brief({}, hours)
    
    # 2. 按股票分组
    grouped = {}
    for entry in all_entries:
        code = entry.get('stock_code', 'unknown')
        if code not in grouped:
            grouped[code] = []
        grouped[code].append(entry)
    
    # 3. 情绪分析
    print("📊 开始情绪分析...")
    analyzer = SentimentAnalyzer()
    
    analyzed_data = {}
    for code, entries in grouped.items():
        analyzed_entries = analyzer.analyze_entries(entries)
        sentiment_summary = analyzer.summarize_sentiment(analyzed_entries)
        
        analyzed_data[code] = {
            "entries": analyzed_entries,
            "sentiment_summary": sentiment_summary
        }
        
        stock_name = entries[0].get('stock_name', code)
        print(f"  {stock_name}: {sentiment_summary['overall']} (评分: {sentiment_summary['avg_score']})")
    
    # 4. 生成报告
    print("📝 生成日报...")
    reporter = DailyReporter()
    
    if output_format == "full":
        report = reporter.generate_report(analyzed_data, hours)
    else:
        report = reporter.generate_brief(analyzed_data, hours)
    
    return report


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="股票舆情监控系统")
    parser.add_argument("--hours", type=int, default=24, help="统计时间范围（小时）")
    parser.add_argument("--format", choices=["brief", "full"], default="brief", help="输出格式")
    parser.add_argument("--test", action="store_true", help="测试模式（48小时）")
    
    args = parser.parse_args()
    
    hours = 48 if args.test else args.hours
    report = run_daily_report(hours=hours, output_format=args.format)
    
    print("\n" + "=" * 50)
    print(report)


if __name__ == "__main__":
    main()
