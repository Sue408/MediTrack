"""
用户API路由层
处理用户相关的HTTP请求
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import base64
import re
from ..db.database import get_db
from ..db.models.user import UserProfile
from ..schemas.user import UserResponse, UserUpdate, UserAvatarUpdate
from ..serves import supabase_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 创建路由器
router = APIRouter(prefix="/users", tags=["用户管理"])

# HTTP Bearer认证
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    获取当前登录用户信息

    从HTTP请求头中提取JWT token，验证后查询用户profile信息。
    邮箱信息从JWT token的payload中提取（存储在Supabase Auth中）。

    :param credentials: HTTP Bearer认证凭证
    :param db: 数据库会话
    :return: 用户信息响应对象
    :raises HTTPException: 401 - token无效或用户不存在
    :raises HTTPException: 500 - 数据处理失败
    """
    token = credentials.credentials

    # 验证JWT token并获取payload
    payload = supabase_service.verify_supabase_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 从payload中提取用户UUID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token中缺少用户UUID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查询用户profile（扩展信息）
    user_profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户profile不存在"
        )

    try:
        # 从JWT token中提取邮箱（存储在Supabase Auth中）
        email = payload.get("email")

        # 构建完整的用户信息响应
        user_data = {
            "id": user_id,
            "username": user_profile.username,
            "email": email,
            "full_name": user_profile.full_name,
            "avatar_url": user_profile.avatar_url,
            "created_at": user_profile.created_at,
            "updated_at": user_profile.updated_at
        }

        return UserResponse(**user_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户数据处理失败"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    获取当前用户信息
    :param current_user: 当前登录用户
    :return: 用户信息
    """
    return current_user


# noinspection DuplicatedCode
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
    # 查询用户profile
    user_profile = db.query(UserProfile).filter(UserProfile.id == current_user.id).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新字段
    if user_data.username is not None:
        # 检查用户名是否已被其他用户使用
        existing = db.query(UserProfile).filter(
            UserProfile.username == user_data.username,
            UserProfile.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
        user_profile.username = user_data.username

    if user_data.full_name is not None:
        user_profile.full_name = user_data.full_name

    # 保存到数据库
    db.add(user_data)
    db.commit()
    db.refresh(user_profile)

    # 构建包含邮箱的完整用户信息
    user_data = {
        "id": str(user_profile.id),
        "username": user_profile.username,
        "email": current_user.email,  # 从当前用户获取邮箱
        "full_name": user_profile.full_name,
        "avatar_url": user_profile.avatar_url,
        "created_at": user_profile.created_at,
        "updated_at": user_profile.updated_at
    }

    return UserResponse(**user_data)


# noinspection DuplicatedCode
@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    avatar_data: UserAvatarUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传用户头像到Supabase Storage
    :param avatar_data: 头像Base64数据
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的用户信息
    """
    # 验证Base64格式
    base64_pattern = r'^data:image/(jpeg|jpg|png|gif|webp);base64,[A-Za-z0-9+/=]+$'
    if not re.match(base64_pattern, avatar_data.avatar):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的Base64图片格式"
        )

    # 提取Base64数据和文件类型
    try:
        header, encoded = avatar_data.avatar.split(',', 1)
        # 提取文件扩展名
        file_ext = header.split('/')[1].split(';')[0]
        if file_ext == 'jpeg':
            file_ext = 'jpg'

        # 解码Base64
        decoded = base64.b64decode(encoded)

        # 限制图片大小为2MB
        max_size = 2 * 1024 * 1024
        if len(decoded) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="图片大小超过2MB限制"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Base64解码失败: {str(e)}"
        )

    # 上传到Supabase Storage
    avatar_url = supabase_service.upload_avatar(current_user.id, decoded, file_ext)
    if not avatar_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="头像上传失败"
        )

    # 更新用户profile
    user_profile = db.query(UserProfile).filter(UserProfile.id == current_user.id).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    user_profile.avatar_url = avatar_url
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)

    # 构建包含邮箱的完整用户信息
    user_data = {
        "id": str(user_profile.id),
        "username": user_profile.username,
        "email": current_user.email,  # 从当前用户获取邮箱
        "full_name": user_profile.full_name,
        "avatar_url": user_profile.avatar_url,
        "created_at": user_profile.created_at,
        "updated_at": user_profile.updated_at
    }

    return UserResponse(**user_data)
