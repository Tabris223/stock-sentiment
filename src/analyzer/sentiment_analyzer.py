"""情绪分析器"""
from typing import Dict, List, Tuple
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """简单的基于词典的情绪分析器"""
    
    def __init__(self):
        # 正面词汇
        self.positive_words = [
            # 业绩相关
            "增长", "盈利", "上涨", "新高", "突破", "翻倍", "暴涨", "大涨",
            "超预期", "利好", "佳绩", "营收增", "净利增", "扭亏", "盈利",
            # 事件相关
            "中标", "签约", "收购", "合作", "获批", "获得", "入选",
            "增持", "回购", "分红", "派息", "股权激励",
            # 行业相关
            "景气", "复苏", "回暖", "需求旺", "订单增", "产能扩张",
            # 市场情绪
            "看好", "推荐", "买入", "增持", "超配", "重仓",
        ]
        
        # 负面词汇
        self.negative_words = [
            # 业绩相关
            "下降", "亏损", "下跌", "暴跌", "大跌", "新低", "腰斩",
            "不及预期", "利空", "业绩降", "营收降", "净利降",
            # 事件相关
            "被查", "处罚", "诉讼", "违约", "减持", "质押", "冻结",
            "召回", "停产", "关闭", "裁员", "离职",
            # 行业相关
            "低迷", "下滑", "萎缩", "产能过剩", "库存高",
            # 市场情绪
            "看空", "卖出", "减持", "低配", "清仓", "避险",
        ]
        
        # 强化词
        self.intensifiers = ["大幅", "显著", "强劲", "强劲", "迅猛", "暴", "狂"]
        
        # 弱化词
        self.diminishers = ["略", "小幅", "微", "有所", "一定程度"]
    
    def _count_words(self, text: str, word_list: List[str]) -> Tuple[int, List[str]]:
        """统计文本中出现的词汇"""
        found = []
        for word in word_list:
            if word in text:
                found.append(word)
        return len(found), found
    
    def analyze(self, text: str) -> Dict:
        """分析文本情绪
        
        返回:
            {
                "sentiment": "positive" | "negative" | "neutral",
                "score": float,  # -1 到 1
                "confidence": float,  # 0 到 1
                "positive_count": int,
                "negative_count": int,
                "positive_words": List[str],
                "negative_words": List[str],
            }
        """
        # 统计正负面词
        pos_count, pos_words = self._count_words(text, self.positive_words)
        neg_count, neg_words = self._count_words(text, self.negative_words)
        
        # 计算分数
        total = pos_count + neg_count
        if total == 0:
            score = 0.0
            sentiment = "neutral"
            confidence = 0.5
        else:
            # 基础分数
            score = (pos_count - neg_count) / total
            
            # 检查强化词
            intensity = 1.0
            for word in self.intensifiers:
                if word in text:
                    intensity *= 1.3
            for word in self.diminishers:
                if word in text:
                    intensity *= 0.7
            
            score = max(-1, min(1, score * intensity))
            
            if score > 0.2:
                sentiment = "positive"
            elif score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            confidence = min(1.0, total / 5)  # 词汇越多越有信心
        
        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "confidence": round(confidence, 3),
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positive_words": pos_words,
            "negative_words": neg_words,
        }
    
    def analyze_entries(self, entries: List[Dict]) -> List[Dict]:
        """分析多条新闻"""
        results = []
        
        for entry in entries:
            text = f"{entry['title']} {entry['summary']}"
            sentiment = self.analyze(text)
            
            result = entry.copy()
            result['sentiment'] = sentiment
            results.append(result)
        
        return results
    
    def summarize_sentiment(self, entries: List[Dict]) -> Dict:
        """汇总情绪统计"""
        if not entries:
            return {
                "total": 0,
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "avg_score": 0,
                "overall": "neutral"
            }
        
        counts = {"positive": 0, "negative": 0, "neutral": 0}
        total_score = 0
        
        for entry in entries:
            s = entry.get('sentiment', {})
            counts[s.get('sentiment', 'neutral')] += 1
            total_score += s.get('score', 0)
        
        avg_score = total_score / len(entries)
        
        # 整体情绪
        if avg_score > 0.15:
            overall = "positive"
        elif avg_score < -0.15:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "total": len(entries),
            "positive": counts["positive"],
            "negative": counts["negative"],
            "neutral": counts["neutral"],
            "avg_score": round(avg_score, 3),
            "overall": overall
        }


def analyze_text(text: str) -> Dict:
    """便捷函数"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


if __name__ == "__main__":
    # 测试
    test_cases = [
        "招商轮船三季度营收大幅增长，净利翻倍，超市场预期",
        "招商轮船股价暴跌，业绩不及预期，遭机构减持",
        "招商轮船发布公告，签署合作协议",
    ]
    
    analyzer = SentimentAnalyzer()
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"\n{text}")
        print(f"  情绪: {result['sentiment']} (得分: {result['score']}, 置信度: {result['confidence']})")
        print(f"  正面词: {result['positive_words']}")
        print(f"  负面词: {result['negative_words']}")
