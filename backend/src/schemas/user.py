"""
用户相关的 Pydantic 模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="真实姓名")


class UserCreate(UserBase):
    """用户注册请求模式"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserLogin(BaseModel):
    """用户登录请求模式"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """用户信息更新请求模式"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="真实姓名")
    password: Optional[str] = Field(None, min_length=6, max_length=50, description="新密码")


class UserAvatarUpdate(BaseModel):
    """用户头像更新请求模式"""
    avatar: str = Field(..., description="头像Base64编码（包含data:image/...;base64,前缀）")


class UserResponse(BaseModel):
    """用户信息响应模式"""
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(None, description="真实姓名")
    avatar: Optional[str] = Field(None, description="头像Base64编码")
    is_active: int = Field(..., description="账户状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True  # 允许从ORM模型创建


class TokenResponse(BaseModel):
    """Token响应模式"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse = Field(..., description="用户信息")
