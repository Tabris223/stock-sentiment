#!/usr/bin/env python3
"""Stock Sentiment API - FastAPI 主入口"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import init_db
from src.api import router as stocks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    init_db()
    yield
    # 关闭时清理资源（如果需要）


app = FastAPI(
    title="Stock Sentiment API",
    description="股票舆情监控系统 - 股票管理 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(stocks_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def root():
    """根路径"""
    return {
        "message": "Stock Sentiment API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
