"""日报生成器"""
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DailyReporter:
    """日报生成器"""
    
    def __init__(self):
        self.emoji_map = {
            "positive": "📈",
            "negative": "📉",
            "neutral": "➖"
        }
        
        self.sentiment_text = {
            "positive": "偏正面",
            "negative": "偏负面",
            "neutral": "中性"
        }
    
    def generate_report(self, stock_data: Dict[str, Dict], hours: int = 24) -> str:
        """生成日报
        
        Args:
            stock_data: {股票代码: {entries: [...], sentiment_summary: {...}}}
            hours: 统计时间范围
        
        Returns:
            Markdown 格式的日报
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        
        lines = []
        lines.append(f"# 📊 股票舆情日报")
        lines.append(f"\n**日期**: {date_str}")
        lines.append(f"**统计周期**: 过去 {hours} 小时")
        lines.append(f"**生成时间**: {time_str}")
        lines.append("")
        
        if not stock_data:
            lines.append("---")
            lines.append("\n⚠️ 今日无相关舆情信息")
            return "\n".join(lines)
        
        # 汇总概览
        lines.append("---")
        lines.append("\n## 📈 概览")
        
        total_news = sum(len(d.get('entries', [])) for d in stock_data.values())
        total_positive = sum(d.get('sentiment_summary', {}).get('positive', 0) for d in stock_data.values())
        total_negative = sum(d.get('sentiment_summary', {}).get('negative', 0) for d in stock_data.values())
        
        lines.append(f"\n- 监控股票: {len(stock_data)} 只")
        lines.append(f"- 相关新闻: {total_news} 条")
        lines.append(f"- 正面舆情: {total_positive} 条")
        lines.append(f"- 负面舆情: {total_negative} 条")
        
        # 各股票详情
        lines.append("")
        lines.append("---")
        lines.append("\n## 📋 各股详情")
        
        for code, data in stock_data.items():
            entries = data.get('entries', [])
            summary = data.get('sentiment_summary', {})
            
            if not entries:
                continue
            
            stock_name = entries[0].get('stock_name', code)
            overall = summary.get('overall', 'neutral')
            avg_score = summary.get('avg_score', 0)
            
            emoji = self.emoji_map.get(overall, "➖")
            sentiment_label = self.sentiment_text.get(overall, "中性")
            
            lines.append(f"\n### {emoji} {stock_name} ({code})")
            lines.append(f"\n**整体情绪**: {sentiment_label} (评分: {avg_score})")
            lines.append(f"\n| 情绪 | 数量 |")
            lines.append(f"|------|------|")
            lines.append(f"| 📈 正面 | {summary.get('positive', 0)} |")
            lines.append(f"| 📉 负面 | {summary.get('negative', 0)} |")
            lines.append(f"| ➖ 中性 | {summary.get('neutral', 0)} |")
            
            # 重要新闻（按情绪强度排序）
            sorted_entries = sorted(
                entries,
                key=lambda x: abs(x.get('sentiment', {}).get('score', 0)),
                reverse=True
            )
            
            lines.append(f"\n**重要新闻**:")
            for i, entry in enumerate(sorted_entries[:5], 1):
                s = entry.get('sentiment', {})
                score = s.get('score', 0)
                s_emoji = self.emoji_map.get(s.get('sentiment', 'neutral'), "➖")
                
                title = entry['title'][:50] + "..." if len(entry['title']) > 50 else entry['title']
                source = entry.get('source', '未知')
                time_str = entry.get('published', '')[:10]
                
                lines.append(f"\n{i}. {s_emoji} **{title}**")
                lines.append(f"   - 来源: {source}")
                lines.append(f"   - 时间: {time_str}")
                lines.append(f"   - 情绪得分: {score}")
                
                # 关键词
                pos_words = s.get('positive_words', [])
                neg_words = s.get('negative_words', [])
                keywords = pos_words + neg_words
                if keywords:
                    lines.append(f"   - 关键词: {', '.join(keywords[:5])}")
        
        # 底部
        lines.append("")
        lines.append("---")
        lines.append("\n*由 Stock Sentiment 系统自动生成*")
        
        return "\n".join(lines)
    
    def generate_brief(self, stock_data: Dict[str, Dict], hours: int = 24) -> str:
        """生成简报（用于飞书等即时通讯）"""
        now = datetime.now()
        date_str = now.strftime("%m-%d")
        
        if not stock_data:
            return f"📅 {date_str} 股票舆情日报\n\n⚠️ 过去 {hours} 小时无相关舆情信息"
        
        # 统计
        total_news = sum(len(d.get('entries', [])) for d in stock_data.values())
        
        lines = []
        lines.append(f"📅 **{date_str} 股票舆情日报**")
        lines.append(f"\n监控 {len(stock_data)} 只股票，共 {total_news} 条相关新闻")
        lines.append("")
        
        for code, data in stock_data.items():
            entries = data.get('entries', [])
            summary = data.get('sentiment_summary', {})
            
            if not entries:
                continue
            
            stock_name = entries[0].get('stock_name', code)
            overall = summary.get('overall', 'neutral')
            emoji = self.emoji_map.get(overall, "➖")
            
            lines.append(f"{emoji} **{stock_name}**")
            lines.append(f"   正面 {summary.get('positive', 0)} / 负面 {summary.get('negative', 0)} / 中性 {summary.get('neutral', 0)}")
            
            # 最重要的一条新闻
            if entries:
                sorted_entries = sorted(
                    entries,
                    key=lambda x: abs(x.get('sentiment', {}).get('score', 0)),
                    reverse=True
                )
                top = sorted_entries[0]
                title = top['title'][:40] + "..." if len(top['title']) > 40 else top['title']
                lines.append(f"   📰 {title}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    reporter = DailyReporter()
    
    test_data = {
        "601872.SH": {
            "entries": [
                {
                    "title": "招商轮船三季度营收大幅增长",
                    "summary": "公司发布三季报...",
                    "source": "财新网",
                    "published": "2026-03-01",
                    "sentiment": {
                        "sentiment": "positive",
                        "score": 0.6,
                        "positive_words": ["增长", "盈利"],
                        "negative_words": []
                    },
                    "stock_name": "招商轮船"
                }
            ],
            "sentiment_summary": {
                "total": 1,
                "positive": 1,
                "negative": 0,
                "neutral": 0,
                "avg_score": 0.6,
                "overall": "positive"
            }
        }
    }
    
    print(reporter.generate_brief(test_data))
