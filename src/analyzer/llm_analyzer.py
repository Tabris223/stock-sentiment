"""LLM 情绪分析器 - 使用大模型进行深度分析"""
from typing import Dict, List
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMSentimentAnalyzer:
    """基于 LLM 的情绪分析器"""
    
    ANALYSIS_PROMPT = """你是一位专业的股票分析师。请分析以下关于【{stock_name}】的新闻，给出你的专业判断。

## 新闻标题
{title}

## 新闻内容
{content}

## 请分析以下维度

1. **情绪倾向**: 正面/负面/中性，给出 -1 到 1 的分数
2. **影响程度**: 高/中/低，这只新闻对股价的影响有多大
3. **影响方向**: 利好/利空/中性
4. **持续时间**: 短期(1-3天)/中期(1-4周)/长期(1季度以上)
5. **关键信息**: 提取 3-5 个关键点
6. **风险提示**: 有什么需要注意的风险
7. **投资建议**: 简短的操作建议（仅供参考）

## 输出格式（JSON）

```json
{{
  "sentiment": "positive/negative/neutral",
  "score": 0.6,
  "impact_level": "high/medium/low",
  "impact_direction": "bullish/bearish/neutral",
  "duration": "short/medium/long",
  "key_points": ["关键点1", "关键点2", "关键点3"],
  "risks": ["风险1", "风险2"],
  "suggestion": "操作建议",
  "reasoning": "判断理由（1-2句话）"
}}
```

请只输出 JSON，不要输出其他内容。"""

    def analyze(self, title: str, content: str, stock_name: str = "招商轮船") -> Dict:
        """使用 LLM 分析单条新闻"""
        
        prompt = self.ANALYSIS_PROMPT.format(
            stock_name=stock_name,
            title=title,
            content=content[:1500]  # 限制长度
        )
        
        try:
            # 使用 sessions_spawn 调用 LLM
            # 这里我们直接用 subprocess 调用一个更简单的方式
            # 或者返回一个默认分析，让主程序用 spawn 调用
            
            # 简化版本：返回待分析的提示
            return {
                "sentiment": "pending",
                "score": 0,
                "prompt": prompt,
                "raw_content": content
            }
            
        except Exception as e:
            logger.error(f"LLM 分析失败: {e}")
            return {
                "sentiment": "error",
                "score": 0,
                "error": str(e)
            }


def analyze_news_with_llm(entries: List[Dict], stock_name: str = "招商轮船") -> List[Dict]:
    """批量分析新闻（返回分析提示，由主程序调用 LLM）"""
    analyzer = LLMSentimentAnalyzer()
    
    results = []
    for entry in entries:
        analysis = analyzer.analyze(
            title=entry['title'],
            content=entry['summary'],
            stock_name=stock_name
        )
        
        result = entry.copy()
        result['llm_analysis'] = analysis
        results.append(result)
    
    return results


if __name__ == "__main__":
    # 测试
    test_news = {
        "title": "航运概念盘初走强 招商轮船涨停",
        "summary": "航运概念盘初走强，招商轮船涨停，中远海能、招商南油等跟涨。消息面上，VLCC运价飙升突破每日17万美元，较年初翻了3倍。"
    }
    
    analyzer = LLMSentimentAnalyzer()
    result = analyzer.analyze(
        title=test_news['title'],
        content=test_news['summary'],
        stock_name="招商轮船"
    )
    
    print(result['prompt'])
