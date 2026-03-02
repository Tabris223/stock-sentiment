"""新闻管理 API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import hashlib
from datetime import datetime
from collections import defaultdict
import logging
from dateutil import parser as date_parser

from ..database import get_db
from ..models.news import News, SourceType
from ..models.stock import Stock
from ..schemas.news import (
    NewsResponse,
    NewsListResponse,
    FetchNewsRequest,
    FetchNewsResponse,
    SourceType as SchemaSourceType
)
from ..schemas.stock import ErrorResponse
from ..fetcher.multi_source_fetcher import MultiSourceFetcher

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/news", tags=["news"])


def calculate_content_hash(title: str, url: str = "") -> str:
    """计算内容哈希用于去重
    
    Args:
        title: 新闻标题
        url: 新闻链接（可选）
    
    Returns:
        SHA256 哈希值（64位字符串）
    """
    content = f"{title}|{url}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


@router.post(
    "/fetch",
    response_model=FetchNewsResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "没有找到股票"},
        500: {"model": ErrorResponse, "description": "抓取失败"}
    },
    summary="手动触发新闻抓取",
    description="从多个数据源抓取新闻并保存到数据库，自动去重。支持个股新闻、财经新闻、央视新闻、研报、资金流等数据源"
)
def fetch_news(
    request: FetchNewsRequest,
    db: Session = Depends(get_db)
):
    """手动触发多数据源新闻抓取
    
    Args:
        request: 抓取请求参数
            - stock_ids: 指定股票ID列表（可选）
            - sources: 指定数据源类型（可选）
            - limit: 每个数据源最多抓取条数
    
    Returns:
        抓取结果统计
    """
    # 准备股票列表（如果需要个股数据）
    stocks = []
    if request.stock_ids:
        stocks = db.query(Stock).filter(Stock.id.in_(request.stock_ids)).all()
        if not stocks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到指定的股票"
            )
    else:
        # 如果没有指定股票，尝试获取所有股票
        stocks = db.query(Stock).limit(50).all()
    
    # 转换为抓取器需要的格式
    stock_list = [{"code": s.code, "name": s.name, "id": s.id} for s in stocks]
    
    # 准备数据源列表
    sources = None
    if request.sources:
        sources = [s.value for s in request.sources]
    
    # 初始化多数据源抓取器
    fetcher = MultiSourceFetcher(enabled_sources=sources)
    
    # 抓取所有数据
    entries = fetcher.fetch_all(
        sources=sources,
        stocks=stock_list,
        limit=request.limit
    )
    
    # 统计信息
    fetched_count = len(entries)
    saved_count = 0
    duplicates = 0
    source_stats = defaultdict(lambda: {"fetched": 0, "saved": 0, "duplicates": 0})
    
    # 保存到数据库（去重）
    for entry in entries:
        try:
            # 计算哈希
            content_hash = calculate_content_hash(
                entry.get('title', ''),
                entry.get('link', '')
            )
            
            # 检查是否已存在
            existing = db.query(News).filter(
                News.content_hash == content_hash
            ).first()
            
            source_type_value = entry.get('source_type', 'stock_news')
            source_stats[source_type_value]["fetched"] += 1
            
            if existing:
                duplicates += 1
                source_stats[source_type_value]["duplicates"] += 1
                continue
            
            # 解析发布时间 - 使用 dateutil.parser 自动处理多种格式
            publish_time = datetime.now()
            if entry.get('published'):
                try:
                    publish_time = date_parser.parse(entry['published'])
                except (ValueError, TypeError) as e:
                    logger.warning(f"时间解析失败，使用当前时间: {entry['published']}, 错误: {e}")
                    publish_time = datetime.now()
            
            # 查找关联的股票ID
            stock_id = None
            if entry.get('stock_code'):
                stock = db.query(Stock).filter(
                    Stock.code.like(f"%{entry['stock_code']}%")
                ).first()
                if stock:
                    stock_id = stock.id
            
            # 创建新闻记录
            news = News(
                stock_id=stock_id,
                title=entry.get('title', ''),
                content=entry.get('summary', ''),
                source=entry.get('source', ''),
                source_type=source_type_value,
                publish_time=publish_time,
                url=entry.get('link', ''),
                content_hash=content_hash
            )
            
            db.add(news)
            saved_count += 1
            source_stats[source_type_value]["saved"] += 1
            
        except Exception as e:
            logger.error(f"保存新闻失败: {e}", exc_info=True)
            continue
    
    # 提交所有更改
    db.commit()
    
    # 构建统计消息
    stats_msg = "\n".join([
        f"  - {k}: 抓取{v['fetched']}条, 保存{v['saved']}条, 重复{v['duplicates']}条"
        for k, v in source_stats.items()
    ])
    
    return FetchNewsResponse(
        fetched_count=fetched_count,
        saved_count=saved_count,
        duplicates=duplicates,
        source_stats=dict(source_stats),
        message=f"成功抓取 {fetched_count} 条数据，保存 {saved_count} 条新记录，跳过 {duplicates} 条重复\n\n各数据源统计:\n{stats_msg}"
    )


@router.get(
    "",
    response_model=NewsListResponse,
    summary="获取新闻列表",
    description="获取所有新闻，按发布时间倒序排列"
)
def list_news(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    source_type: Optional[SchemaSourceType] = Query(None, description="按来源类型筛选"),
    db: Session = Depends(get_db)
):
    """获取新闻列表
    
    Args:
        skip: 跳过数量
        limit: 返回数量
        source_type: 按来源类型筛选（可选）
    """
    query = db.query(News)
    
    # 按来源类型筛选
    if source_type:
        query = query.filter(News.source_type == source_type.value)
    
    total = query.count()
    news = query.order_by(
        News.publish_time.desc()
    ).offset(skip).limit(limit).all()
    
    return NewsListResponse(
        total=total,
        news=news
    )


@router.get(
    "/stock/{stock_id}",
    response_model=NewsListResponse,
    responses={
        404: {"model": ErrorResponse, "description": "股票不存在"}
    },
    summary="获取指定股票的新闻",
    description="获取某只股票的所有新闻"
)
def get_stock_news(
    stock_id: int,
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    db: Session = Depends(get_db)
):
    """获取指定股票的新闻"""
    # 检查股票是否存在
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"股票 ID {stock_id} 不存在"
        )
    
    # 查询该股票的新闻
    total = db.query(News).filter(News.stock_id == stock_id).count()
    news = db.query(News).filter(
        News.stock_id == stock_id
    ).order_by(
        News.publish_time.desc()
    ).offset(skip).limit(limit).all()
    
    return NewsListResponse(
        total=total,
        news=news
    )
