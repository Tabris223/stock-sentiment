"""新闻相关的 Pydantic schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    """新闻来源类型"""
    STOCK_NEWS = "stock_news"       # 个股新闻
    FINANCE_NEWS = "finance_news"   # 财经新闻
    CCTV_NEWS = "cctv_news"         # 央视新闻
    RESEARCH = "research"           # 研报
    FUND_FLOW = "fund_flow"         # 资金流


class NewsBase(BaseModel):
    """新闻基础模型"""
    title: str = Field(..., description="新闻标题")
    content: Optional[str] = Field(None, description="新闻内容")
    source: Optional[str] = Field(None, description="新闻来源")
    source_type: Optional[SourceType] = Field(SourceType.STOCK_NEWS, description="来源类型")
    publish_time: Optional[datetime] = Field(None, description="发布时间")
    url: Optional[str] = Field(None, description="原始链接")


class NewsCreate(NewsBase):
    """创建新闻请求模型"""
    stock_id: Optional[int] = Field(None, description="关联股票ID（财经新闻可为空）")


class NewsResponse(NewsBase):
    """新闻响应模型"""
    id: int
    stock_id: Optional[int] = None
    content_hash: str
    created_at: datetime

    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    """新闻列表响应模型"""
    total: int
    news: List[NewsResponse]


class FetchNewsRequest(BaseModel):
    """抓取新闻请求模型"""
    stock_ids: Optional[List[int]] = Field(None, description="指定股票ID列表，为空则抓取所有")
    sources: Optional[List[SourceType]] = Field(
        None, 
        description="指定数据源类型列表，为空则抓取所有。可选：stock_news, finance_news, cctv_news, research, fund_flow"
    )
    limit: Optional[int] = Field(50, description="每个数据源最多抓取新闻数", ge=1, le=200)


class FetchNewsResponse(BaseModel):
    """抓取新闻响应模型"""
    fetched_count: int = Field(..., description="成功抓取数量")
    saved_count: int = Field(..., description="新保存数量（去重后）")
    duplicates: int = Field(..., description="重复数量")
    source_stats: Optional[dict] = Field(None, description="各数据源抓取统计")
    message: str = Field(..., description="处理结果消息")
