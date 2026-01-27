"""
API路由模块
导出所有API路由器
"""
from .user import router as user_router
from .medication import router as medication_router
from .reminder import router as reminder_router

__all__ = ["user_router", "medication_router", "reminder_router"]
