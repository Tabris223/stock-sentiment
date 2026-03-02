"""多数据源新闻抓取器"""
import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SourceType(str, Enum):
    """数据源类型"""
    STOCK_NEWS = "stock_news"       # 个股新闻
    FINANCE_NEWS = "finance_news"   # 财经新闻
    CCTV_NEWS = "cctv_news"         # 央视新闻
    RESEARCH = "research"           # 研报
    FUND_FLOW = "fund_flow"         # 资金流


class MultiSourceFetcher:
    """统一多数据源抓取器"""
    
    def __init__(self, enabled_sources: Optional[List[str]] = None):
        """初始化
        
        Args:
            enabled_sources: 启用的数据源列表，为空则启用所有
        """
        self.enabled_sources = enabled_sources or list(SourceType)
    
    def _is_enabled(self, source_type: SourceType) -> bool:
        """检查数据源是否启用"""
        return source_type.value in [s.value if isinstance(s, SourceType) else s for s in self.enabled_sources]
    
    def _parse_publish_time(self, time_value) -> str:
        """解析发布时间字段
        
        Args:
            time_value: 时间字段值（可能是字符串、datetime 等）
        
        Returns:
            格式化的时间字符串
        """
        if not time_value:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 如果已经是 datetime 对象
        if isinstance(time_value, datetime):
            return time_value.strftime("%Y-%m-%d %H:%M:%S")
        
        # 尝试转为字符串
        time_str = str(time_value)
        if not time_str or time_str == 'nan':
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return time_str
    
    def _get_market(self, stock_code: str) -> str:
        """根据股票代码判断市场
        
        Args:
            stock_code: 股票代码（纯数字）
        
        Returns:
            市场代码：sh=上海，sz=深圳
        """
        if stock_code.startswith(('60', '68')):
            return "sh"  # 上海
        elif stock_code.startswith(('00', '30')):
            return "sz"  # 深圳
        return "sh"  # 默认上海
    
    # ========== P0 数据源 ==========
    
    def fetch_stock_news_em(self, stock_code: str, stock_name: str, limit: int = 50) -> List[Dict]:
        """获取东财个股新闻（原有数据源）
        
        Args:
            stock_code: 股票代码（纯数字）
            stock_name: 股票名称
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.STOCK_NEWS):
            return []
        
        entries = []
        try:
            logger.info(f"[个股新闻] 获取 {stock_name}({stock_code}) 新闻...")
            df = ak.stock_news_em(symbol=stock_name)
            
            if df is not None and not df.empty:
                for _, row in df.head(limit).iterrows():
                    entries.append({
                        "title": str(row.get("新闻标题", "")),
                        "link": str(row.get("新闻链接", "")),
                        "summary": str(row.get("新闻内容", ""))[:500],
                        "published": self._parse_publish_time(row.get("发布时间")),
                        "source": str(row.get("来源", "东方财富")),
                        "source_type": SourceType.STOCK_NEWS.value,
                        "stock_code": stock_code,
                        "stock_name": stock_name,
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条个股新闻")
        except Exception as e:
            logger.warning(f"  ✗ 个股新闻获取失败: {e}")
        
        return entries
    
    def fetch_finance_news_cx(self, limit: int = 100) -> List[Dict]:
        """获取东财财经新闻（100条综合新闻）- P0 必须
        
        Args:
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.FINANCE_NEWS):
            return []
        
        entries = []
        try:
            logger.info(f"[财经新闻] 获取东财综合财经新闻...")
            df = ak.stock_news_main_cx()
            
            if df is not None and not df.empty:
                for _, row in df.head(limit).iterrows():
                    # ak.stock_news_main_cx() 返回列名: ['tag', 'summary', 'url']
                    entries.append({
                        "title": str(row.get("tag", "")),
                        "link": str(row.get("url", "")),
                        "summary": str(row.get("summary", ""))[:500],
                        "published": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "财新",
                        "source_type": SourceType.FINANCE_NEWS.value,
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条财经新闻")
        except Exception as e:
            logger.warning(f"  ✗ 财经新闻获取失败: {e}")
        
        return entries
    
    def fetch_cctv_news(self, limit: int = 50) -> List[Dict]:
        """获取央视财经新闻 - P0 必须
        
        Args:
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.CCTV_NEWS):
            return []
        
        entries = []
        try:
            logger.info(f"[央视新闻] 获取央视财经新闻...")
            df = ak.news_cctv()
            
            if df is not None and not df.empty:
                for _, row in df.head(limit).iterrows():
                    entries.append({
                        "title": str(row.get("title", "")),
                        "link": str(row.get("link", "")),
                        "summary": str(row.get("content", ""))[:500],
                        "published": self._parse_publish_time(row.get("date")),
                        "source": "央视财经",
                        "source_type": SourceType.CCTV_NEWS.value,
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条央视新闻")
        except Exception as e:
            logger.warning(f"  ✗ 央视新闻获取失败: {e}")
        
        return entries
    
    # ========== P1 数据源 ==========
    
    def fetch_research_report(self, limit: int = 50) -> List[Dict]:
        """获取研报摘要 - P1 重要
        
        Args:
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.RESEARCH):
            return []
        
        entries = []
        try:
            logger.info(f"[研报] 获取研究报告摘要...")
            df = ak.stock_research_report_em()
            
            if df is not None and not df.empty:
                for _, row in df.head(limit).iterrows():
                    entries.append({
                        "title": str(row.get("标题", "")),
                        "link": str(row.get("链接", "")),
                        "summary": str(row.get("摘要", ""))[:500],
                        "published": self._parse_publish_time(row.get("发布日期")),
                        "source": str(row.get("机构", "券商研报")),
                        "source_type": SourceType.RESEARCH.value,
                        "stock_code": str(row.get("代码", "")),
                        "stock_name": str(row.get("名称", "")),
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条研报")
        except Exception as e:
            logger.warning(f"  ✗ 研报获取失败: {e}")
        
        return entries
    
    def fetch_sector_fund_flow(self, limit: int = 50) -> List[Dict]:
        """获取行业资金流 - P1 重要（东方财富接口，备用）
        
        Args:
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.FUND_FLOW):
            return []
        
        entries = []
        try:
            logger.info(f"[资金流] 获取行业资金流（东方财富）...")
            df = ak.stock_sector_fund_flow_rank(indicator="今日")
            
            if df is not None and not df.empty:
                for _, row in df.head(limit).iterrows():
                    # 资金流数据通常为当日，优先使用数据源日期字段
                    publish_time = self._parse_publish_time(row.get("日期"))
                    if not row.get("日期"):
                        # 如果没有日期字段，使用当日日期（因为查询的是"今日"数据）
                        publish_time = datetime.now().strftime("%Y-%m-%d")
                    
                    entries.append({
                        "title": f"【{row.get('名称', '')}】{row.get('主力净流入', '')}万",
                        "link": "",
                        "summary": f"主力净流入: {row.get('主力净流入', '')}万, 涨跌幅: {row.get('涨跌幅', '')}%",
                        "published": publish_time,
                        "source": "东方财富",
                        "source_type": SourceType.FUND_FLOW.value,
                        "sector": str(row.get("名称", "")),
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条行业资金流")
        except Exception as e:
            logger.warning(f"  ✗ 行业资金流获取失败: {e}")
        
        return entries
    
    def fetch_ths_industry_fund_flow(self, limit: int = 100, period: str = "即时") -> List[Dict]:
        """同花顺行业资金流
        
        Args:
            limit: 最多返回条数
            period: 时间周期（即时/3日/5日/10日/20日）
        """
        if not self._is_enabled(SourceType.FUND_FLOW):
            return []
        
        try:
            logger.info(f"[资金流] 获取同花顺行业资金流（{period}）...")
            df = ak.stock_fund_flow_industry(symbol=period)
            
            if df is not None and not df.empty:
                entries = []
                for _, row in df.head(limit).iterrows():
                    sector_name = str(row.get("行业", ""))
                    net_amount = row.get("净额", "N/A")
                    entries.append({
                        "title": f"【{sector_name}】净额: {net_amount}亿",
                        "link": "",
                        "summary": f"主力净流入: {net_amount}亿, 涨跌幅: {row.get('行业-涨跌幅', 'N/A')}%, 领涨股: {row.get('领涨股', 'N/A')}",
                        "published": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "同花顺",
                        "source_type": SourceType.FUND_FLOW.value,
                        "sector": sector_name,
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条同花顺行业资金流")
                return entries
            else:
                logger.warning(f"  ✗ 同花顺行业资金流数据为空")
                return []
        except Exception as e:
            logger.warning(f"  ✗ 同花顺行业资金流获取失败: {e}")
            return []
    
    def fetch_ths_individual_fund_flow(self, limit: int = 100, period: str = "即时") -> List[Dict]:
        """同花顺个股资金流
        
        Args:
            limit: 最多返回条数
            period: 时间周期（即时/3日/5日/10日/20日）
        """
        if not self._is_enabled(SourceType.FUND_FLOW):
            return []
        
        try:
            logger.info(f"[资金流] 获取同花顺个股资金流（{period}）...")
            df = ak.stock_fund_flow_individual(symbol=period)
            
            if df is not None and not df.empty:
                entries = []
                for _, row in df.head(limit).iterrows():
                    stock_name = str(row.get("股票简称", ""))
                    net_amount = row.get("净额", "N/A")
                    entries.append({
                        "title": f"【{stock_name}】净额: {net_amount}",
                        "link": "",
                        "summary": f"主力净流入: {net_amount}, 涨跌幅: {row.get('涨跌幅', 'N/A')}, 换手率: {row.get('换手率', 'N/A')}",
                        "published": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "同花顺",
                        "source_type": SourceType.FUND_FLOW.value,
                        "stock_code": str(row.get("股票代码", "")),
                        "stock_name": stock_name,
                    })
                logger.info(f"  ✓ 获取 {len(entries)} 条同花顺个股资金流")
                return entries
            else:
                logger.warning(f"  ✗ 同花顺个股资金流数据为空")
                return []
        except Exception as e:
            logger.warning(f"  ✗ 同花顺个股资金流获取失败: {e}")
            return []
    
    def fetch_individual_fund_flow(self, stock_code: str, stock_name: str, limit: int = 50) -> List[Dict]:
        """获取个股资金流 - P1 重要
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            limit: 最多返回条数
        """
        if not self._is_enabled(SourceType.FUND_FLOW):
            return []
        
        entries = []
        try:
            logger.info(f"[资金流] 获取 {stock_name}({stock_code}) 资金流...")
            market = self._get_market(stock_code)
            df = ak.stock_individual_fund_flow(stock=stock_code, market=market)
            
            if df is not None and not df.empty:
                # 获取最新一条记录
                latest = df.head(1).iloc[0]
                entries.append({
                    "title": f"【{stock_name}】主力净流入 {latest.get('主力净流入-净额', '')}万",
                    "link": "",
                    "summary": f"主力净流入: {latest.get('主力净流入-净额', '')}万, 超大单: {latest.get('超大单净流入-净额', '')}万, 大单: {latest.get('大单净流入-净额', '')}万",
                    "published": self._parse_publish_time(latest.get("日期")),
                    "source": "东方财富",
                    "source_type": SourceType.FUND_FLOW.value,
                    "stock_code": stock_code,
                    "stock_name": stock_name,
                })
                logger.info(f"  ✓ 获取 {len(entries)} 条个股资金流")
        except Exception as e:
            logger.warning(f"  ✗ 个股资金流获取失败: {e}")
        
        return entries
    
    # ========== 统一抓取接口 ==========
    
    def fetch_all(self, 
                  sources: Optional[List[str]] = None, 
                  stocks: Optional[List[Dict]] = None,
                  limit: int = 50) -> List[Dict]:
        """统一抓取所有启用的数据源
        
        Args:
            sources: 指定数据源类型列表，为空则使用 enabled_sources
            stocks: 股票列表 [{"code": "601872", "name": "招商轮船"}]
            limit: 每个数据源最多抓取条数
        
        Returns:
            所有新闻条目列表
        """
        if sources:
            original = self.enabled_sources
            self.enabled_sources = sources
        
        all_entries = []
        
        try:
            # 1. 个股新闻（如果有股票列表）
            if stocks:
                for stock in stocks:
                    code = stock.get('code', '').split('.')[0]  # 去掉后缀
                    name = stock.get('name', '')
                    entries = self.fetch_stock_news_em(code, name, limit)
                    all_entries.extend(entries)
                    
                    # 个股资金流
                    fund_entries = self.fetch_individual_fund_flow(code, name, limit)
                    all_entries.extend(fund_entries)
            
            # 2. 财经新闻
            entries = self.fetch_finance_news_cx(limit)
            all_entries.extend(entries)
            
            # 3. 央视新闻
            entries = self.fetch_cctv_news(limit)
            all_entries.extend(entries)
            
            # 4. 研报
            entries = self.fetch_research_report(limit)
            all_entries.extend(entries)
            
            # 5. 行业资金流（使用同花顺接口替代东方财富）
            entries = self.fetch_ths_industry_fund_flow(limit=limit)
            all_entries.extend(entries)
            
            # 6. 个股资金流（同花顺）
            entries = self.fetch_ths_individual_fund_flow(limit=limit)
            all_entries.extend(entries)
            
        finally:
            if sources:
                self.enabled_sources = original
        
        logger.info(f"\n✅ 总计获取 {len(all_entries)} 条数据")
        return all_entries


# ========== 便捷函数 ==========

def fetch_multi_source(sources: Optional[List[str]] = None, 
                       stocks: Optional[List[Dict]] = None,
                       limit: int = 50) -> List[Dict]:
    """便捷函数：抓取多数据源新闻"""
    fetcher = MultiSourceFetcher(sources)
    return fetcher.fetch_all(sources, stocks, limit)


# ========== 测试脚本 ==========

if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("多数据源抓取器测试")
    print("=" * 60)
    
    fetcher = MultiSourceFetcher()
    
    # 测试单个数据源
    print("\n1. 测试个股新闻（招商轮船）")
    entries = fetcher.fetch_stock_news_em("601872", "招商轮船", 5)
    print(f"   结果: {len(entries)} 条")
    
    print("\n2. 测试财经新闻")
    entries = fetcher.fetch_finance_news_cx(5)
    print(f"   结果: {len(entries)} 条")
    
    print("\n3. 测试央视新闻")
    entries = fetcher.fetch_cctv_news(5)
    print(f"   结果: {len(entries)} 条")
    
    print("\n4. 测试研报")
    entries = fetcher.fetch_research_report(5)
    print(f"   结果: {len(entries)} 条")
    
    print("\n5. 测试行业资金流")
    entries = fetcher.fetch_sector_fund_flow(5)
    print(f"   结果: {len(entries)} 条")
    
    print("\n6. 测试个股资金流")
    entries = fetcher.fetch_individual_fund_flow("601872", "招商轮船")
    print(f"   结果: {len(entries)} 条")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
