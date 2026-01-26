"""
用户API路由层
处理用户相关的HTTP请求
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import base64
import re

from ..db.database import get_db
from ..schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    TokenResponse,
    UserAvatarUpdate
)
from ..serves import user_service
from fastapi.security import OAuth2PasswordBearer

# 创建路由器
router = APIRouter(prefix="/user", tags=["用户管理"])

# OAuth2密码bearer认证 (tokenUrl指定来源)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    获取当前登录用户
    :param token: JWT令牌
    :param db: 数据库会话
    :return: 当前用户信息
    """
    # 解码token
    payload = user_service.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取用户ID
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查询用户
    user = user_service.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse.model_validate(user)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    :param user_data: 用户注册数据
    :param db: 数据库会话
    :return: 用户信息和访问令牌
    """
    # 检查用户名是否已存在
    existing_user = user_service.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    existing_email = user_service.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    # 创建用户
    print(user_data)
    user = user_service.create_user(db, user_data)

    # 生成访问令牌
    access_token = user_service.create_access_token(
        data={"sub": user.id}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    :param login_data: 登录数据
    :param db: 数据库会话
    :return: 用户信息和访问令牌
    """
    # 验证用户
    user = user_service.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查账户是否激活
    if user.is_active != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )

    # 生成访问令牌
    access_token = user_service.create_access_token(
        data={"sub": user.id}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    获取当前用户信息
    :param current_user: 当前登录用户
    :return: 用户信息
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息
    :param user_data: 更新数据
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的用户信息
    """
    # 如果更新邮箱，检查邮箱是否已被其他用户使用
    if user_data.email:
        existing_email = user_service.get_user_by_email(db, user_data.email)
        if existing_email and existing_email.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被其他用户使用"
            )

    # 更新用户信息
    updated_user = user_service.update_user(db, current_user.id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return UserResponse.model_validate(updated_user)


@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    avatar_data: UserAvatarUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传用户头像（Base64编码）
    :param avatar_data: 头像Base64数据
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的用户信息
    """
    # 验证Base64格式（应包含data:image/...;base64,前缀）
    base64_pattern = r'^data:image/(jpeg|jpg|png|gif|webp);base64,[A-Za-z0-9+/=]+$'
    if not re.match(base64_pattern, avatar_data.avatar):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的Base64图片格式，应包含data:image/...;base64,前缀"
        )

    # 提取Base64数据部分（去掉前缀）
    try:
        # 分离前缀和数据
        header, encoded = avatar_data.avatar.split(',', 1)

        # 验证Base64数据并检查大小
        decoded = base64.b64decode(encoded)

        # 限制图片大小为5MB
        max_size = 5 * 1024 * 1024  # 5MB
        if len(decoded) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="图片大小超过5MB限制"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Base64解码失败: {str(e)}"
        )

    # 更新用户头像
    updated_user = user_service.update_user_avatar(db, current_user.id, avatar_data.avatar)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return UserResponse.model_validate(updated_user)
