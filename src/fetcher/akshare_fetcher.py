"""AkShare 新闻抓取器"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AkShareNewsFetcher:
    """基于 AkShare 的新闻抓取器"""
    
    def __init__(self):
        pass
    
    def fetch_stock_news(self, stock_code: str, stock_name: str) -> List[Dict]:
        """获取单只股票相关新闻
        
        Args:
            stock_code: 股票代码，如 "601872"
            stock_name: 股票名称，如 "招商轮船"
        
        Returns:
            新闻列表
        """
        entries = []
        
        try:
            # 方法1：获取个股新闻
            logger.info(f"获取 {stock_name} 新闻...")
            
            # 东方财富个股新闻
            try:
                df = ak.stock_news_em(symbol=stock_name)
                if df is not None and not df.empty:
                    for _, row in df.iterrows():
                        entries.append({
                            "title": str(row.get("新闻标题", "")),
                            "link": str(row.get("新闻链接", "")),
                            "summary": str(row.get("新闻内容", ""))[:500],
                            "published": str(row.get("发布时间", "")),
                            "source": str(row.get("来源", "东方财富")),
                            "category": "stock_news",
                            "stock_code": stock_code,
                            "stock_name": stock_name,
                        })
                    logger.info(f"  获取 {len(df)} 条个股新闻")
            except Exception as e:
                logger.warning(f"  个股新闻获取失败: {e}")
            
        except Exception as e:
            logger.error(f"新闻抓取失败: {e}")
        
        return entries
    
    def fetch_cctv_news(self) -> List[Dict]:
        """获取央视财经新闻"""
        entries = []
        
        try:
            logger.info("获取央视财经新闻...")
            df = ak.stock_cctv_news()
            
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    entries.append({
                        "title": str(row.get("title", "")),
                        "link": "",
                        "summary": str(row.get("content", ""))[:500],
                        "published": str(row.get("date", "")),
                        "source": "央视财经",
                        "category": "cctv_news",
                    })
                logger.info(f"  获取 {len(df)} 条央视新闻")
                
        except Exception as e:
            logger.warning(f"央视新闻获取失败: {e}")
        
        return entries
    
    def fetch_financial_news(self) -> List[Dict]:
        """获取综合财经新闻"""
        entries = []
        
        try:
            # 东方财富财经新闻
            logger.info("获取东方财富财经新闻...")
            df = ak.stock_news_em(symbol="财经新闻")
            
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    entries.append({
                        "title": str(row.get("新闻标题", "")),
                        "link": str(row.get("新闻链接", "")),
                        "summary": str(row.get("新闻内容", ""))[:500],
                        "published": str(row.get("发布时间", "")),
                        "source": str(row.get("来源", "东方财富")),
                        "category": "finance_news",
                    })
                logger.info(f"  获取 {len(df)} 条财经新闻")
                
        except Exception as e:
            logger.warning(f"财经新闻获取失败: {e}")
        
        return entries
    
    def fetch_all(self, stocks: List[Dict]) -> List[Dict]:
        """获取所有新闻
        
        Args:
            stocks: 股票列表 [{"code": "601872.SH", "name": "招商轮船", "keywords": [...]}]
        """
        all_entries = []
        
        # 1. 获取各股票新闻
        for stock in stocks:
            code = stock['code'].split('.')[0]  # 去掉后缀
            name = stock['name']
            entries = self.fetch_stock_news(code, name)
            all_entries.extend(entries)
        
        # 2. 获取综合财经新闻
        # finance_entries = self.fetch_financial_news()
        # all_entries.extend(finance_entries)
        
        return all_entries


def fetch_news(stock_code: str, stock_name: str) -> List[Dict]:
    """便捷函数"""
    fetcher = AkShareNewsFetcher()
    return fetcher.fetch_stock_news(stock_code, stock_name)


if __name__ == "__main__":
    # 测试
    fetcher = AkShareNewsFetcher()
    entries = fetcher.fetch_stock_news("601872", "招商轮船")
    
    print(f"\n获取到 {len(entries)} 条新闻:")
    for e in entries[:5]:
        print(f"  - [{e['source']}] {e['title'][:50]}")
