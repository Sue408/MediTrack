"""
API路由模块
导出所有API路由器
"""
from .user import router as user_router

__all__ = ["user_router"]
