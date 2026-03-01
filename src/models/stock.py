"""股票数据模型"""
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from ..database import Base


class Stock(Base):
    """股票表"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    keywords = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Stock(code={self.code}, name={self.name})>"
