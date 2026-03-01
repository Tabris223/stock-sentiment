"""RSS 抓取器"""
import feedparser
import yaml
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSFetcher:
    """RSS 订阅抓取器"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = Path(__file__).parent.parent.parent / "config"
        
        self.config_dir = Path(config_dir)
        self.feeds_config = self._load_yaml(self.config_dir / "feeds.yaml")
        self.stocks_config = self._load_yaml(self.config_dir / "stocks.yaml")
        
        # 缓存目录
        self.cache_dir = Path(__file__).parent.parent.parent / "feeds" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_yaml(self, path: Path) -> dict:
        """加载 YAML 配置"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _get_cache_path(self, feed_name: str) -> Path:
        """获取缓存文件路径"""
        safe_name = hashlib.md5(feed_name.encode()).hexdigest()
        return self.cache_dir / f"{safe_name}.json"
    
    def _load_cache(self, feed_name: str) -> Dict:
        """加载缓存"""
        cache_path = self._get_cache_path(feed_name)
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"entries": [], "last_fetch": None}
    
    def _save_cache(self, feed_name: str, data: Dict):
        """保存缓存"""
        cache_path = self._get_cache_path(feed_name)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _match_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """检查文本是否包含关键词"""
        matched = []
        text_lower = text.lower()
        for kw in keywords:
            if kw.lower() in text_lower:
                matched.append(kw)
        return matched
    
    def fetch_feed(self, feed: Dict, hours: int = 24) -> List[Dict]:
        """抓取单个 RSS 源"""
        entries = []
        
        try:
            logger.info(f"抓取 RSS: {feed['name']}")
            parsed = feedparser.parse(feed['url'])
            
            if parsed.bozo and parsed.bozo_exception:
                logger.warning(f"RSS 解析警告 [{feed['name']}]: {parsed.bozo_exception}")
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            for entry in parsed.entries:
                # 解析发布时间
                published = entry.get('published_parsed')
                if published:
                    pub_date = datetime(*published[:6])
                else:
                    pub_date = datetime.now()
                
                # 过滤时间范围
                if pub_date < cutoff_time:
                    continue
                
                entries.append({
                    "title": entry.get('title', ''),
                    "link": entry.get('link', ''),
                    "summary": entry.get('summary', entry.get('description', '')),
                    "published": pub_date.isoformat(),
                    "source": feed['name'],
                    "category": feed.get('category', 'unknown')
                })
            
            logger.info(f"  获取 {len(entries)} 条新内容")
            
        except Exception as e:
            logger.error(f"抓取失败 [{feed['name']}]: {e}")
        
        return entries
    
    def fetch_all(self, hours: int = 24) -> List[Dict]:
        """抓取所有 RSS 源"""
        all_entries = []
        
        for feed in self.feeds_config['feeds']:
            entries = self.fetch_feed(feed, hours)
            all_entries.extend(entries)
        
        return all_entries
    
    def filter_by_stocks(self, entries: List[Dict]) -> Dict[str, List[Dict]]:
        """按股票过滤新闻"""
        results = {}
        
        for stock in self.stocks_config['stocks']:
            code = stock['code']
            name = stock['name']
            keywords = stock.get('keywords', [name])
            
            matched_entries = []
            for entry in entries:
                text = f"{entry['title']} {entry['summary']}"
                matched_kw = self._match_keywords(text, keywords)
                
                if matched_kw:
                    entry_copy = entry.copy()
                    entry_copy['matched_keywords'] = matched_kw
                    entry_copy['stock_code'] = code
                    entry_copy['stock_name'] = name
                    matched_entries.append(entry_copy)
            
            if matched_entries:
                results[code] = matched_entries
                logger.info(f"股票 [{name}] 匹配到 {len(matched_entries)} 条新闻")
        
        return results


def fetch_and_filter(hours: int = 24) -> Dict[str, List[Dict]]:
    """便捷函数：抓取并过滤"""
    fetcher = RSSFetcher()
    all_entries = fetcher.fetch_all(hours)
    return fetcher.filter_by_stocks(all_entries)


if __name__ == "__main__":
    # 测试
    results = fetch_and_filter(hours=48)
    for code, entries in results.items():
        print(f"\n{code}: {len(entries)} 条")
        for e in entries[:3]:
            print(f"  - [{e['source']}] {e['title']}")
