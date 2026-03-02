"""新闻数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Index, LargeBinary
from sqlalchemy.sql import func
from ..database import Base
import enum


class SourceType(str, enum.Enum):
    """新闻来源类型"""
    STOCK_NEWS = "stock_news"       # 个股新闻
    FINANCE_NEWS = "finance_news"   # 财经新闻
    CCTV_NEWS = "cctv_news"         # 央视新闻
    RESEARCH = "research"           # 研报
    FUND_FLOW = "fund_flow"         # 资金流


class News(Base):
    """新闻表"""
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=True, index=True)  # 改为 nullable，因为财经新闻不关联个股
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)
    source_type = Column(Enum(SourceType), nullable=False, default=SourceType.STOCK_NEWS, index=True)  # 新增字段
    publish_time = Column(DateTime(timezone=True), nullable=True, index=True)
    url = Column(String(1000), nullable=True)
    content_hash = Column(String(64), unique=True, nullable=False, index=True)
    embedding = Column(LargeBinary, nullable=True)  # 向量嵌入（用于语义去重）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 复合索引：优化按股票+时间查询的性能
    __table_args__ = (
        Index('idx_stock_publish', 'stock_id', 'publish_time'),
    )

    def __repr__(self):
        return f"<News(id={self.id}, source_type={self.source_type}, title={self.title[:30]}...)>"
