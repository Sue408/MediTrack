"""
Schemas 模块
导出所有 Pydantic 模式
"""
from .user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserAvatarUpdate,
    UserResponse,
    TokenResponse
)
from .medication import (
    MedicationBase,
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserAvatarUpdate",
    "UserResponse",
    "TokenResponse",
    "MedicationBase",
    "MedicationCreate",
    "MedicationUpdate",
    "MedicationResponse"
]
