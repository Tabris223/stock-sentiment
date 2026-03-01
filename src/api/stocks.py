"""股票管理 API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.stock import Stock
from ..schemas.stock import StockCreate, StockResponse, StockListResponse, ErrorResponse

router = APIRouter(prefix="/stocks", tags=["stocks"])

MAX_STOCKS = 10


@router.post(
    "",
    response_model=StockResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "已达到最大股票数量限制或代码已存在"},
        422: {"model": ErrorResponse, "description": "参数验证失败"}
    },
    summary="添加股票",
    description="添加一只新股票到监控列表。最多支持 10 只股票。"
)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    """添加股票"""
    # 检查数量限制
    current_count = db.query(Stock).count()
    if current_count >= MAX_STOCKS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"已达到最大股票数量限制（{MAX_STOCKS}只）"
        )
    
    # 检查代码是否已存在
    existing = db.query(Stock).filter(Stock.code == stock.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"股票代码 {stock.code} 已存在"
        )
    
    # 创建股票记录（keywords 直接存 Python 列表，SQLAlchemy JSON 类型自动处理）
    db_stock = Stock(
        code=stock.code,
        name=stock.name,
        keywords=stock.keywords
    )
    
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    
    return db_stock


@router.get(
    "",
    response_model=StockListResponse,
    summary="获取股票列表",
    description="获取所有监控中的股票列表"
)
def list_stocks(db: Session = Depends(get_db)):
    """获取股票列表"""
    stocks = db.query(Stock).order_by(Stock.created_at.desc()).all()
    
    return StockListResponse(
        total=len(stocks),
        stocks=stocks
    )


@router.get(
    "/{stock_id}",
    response_model=StockResponse,
    responses={
        404: {"model": ErrorResponse, "description": "股票不存在"}
    },
    summary="获取单个股票",
    description="根据 ID 获取股票详情"
)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    """获取单个股票"""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"股票 ID {stock_id} 不存在"
        )
    
    return stock


@router.delete(
    "/{stock_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "股票不存在"}
    },
    summary="删除股票",
    description="从监控列表中删除股票"
)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """删除股票"""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"股票 ID {stock_id} 不存在"
        )
    
    db.delete(stock)
    db.commit()
    
    return None
