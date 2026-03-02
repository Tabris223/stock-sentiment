"""API 路由"""
from fastapi import APIRouter
from .stocks import router as stocks_router
from .news import router as news_router

# 创建主路由器
router = APIRouter()

# 注册子路由
router.include_router(stocks_router)
router.include_router(news_router)

__all__ = ["router"]
