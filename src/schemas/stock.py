"""股票相关的 Pydantic schemas"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re


class StockBase(BaseModel):
    """股票基础模型"""
    code: str = Field(..., description="股票代码", examples=["600000.SH"])
    name: str = Field(..., description="股票名称", examples=["浦发银行"])
    keywords: Optional[List[str]] = Field(default=None, description="关键词列表")

    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        """验证股票代码格式"""
        pattern = r'^\d{6}\.(SZ|SH)$'
        if not re.match(pattern, v):
            raise ValueError('股票代码格式错误，应为 000001.SZ 或 600000.SH 格式')
        return v


class StockCreate(StockBase):
    """创建股票请求模型"""
    pass


class StockResponse(StockBase):
    """股票响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StockListResponse(BaseModel):
    """股票列表响应模型"""
    total: int
    stocks: List[StockResponse]


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: Optional[str] = None
