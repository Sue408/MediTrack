"""
用户业务逻辑层
处理用户相关的业务逻辑，包括JWT生成等
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..db.models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.config import config

# JWT配置
SECRET_KEY = config.SECRET_KEY if hasattr(config, 'SECRET_KEY') else "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    :param data: 要编码的数据
    :param expires_delta: 过期时间增量
    :return: JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码JWT访问令牌
    :param token: JWT令牌
    :return: 解码后的数据，失败返回None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e: # noqa
        return None


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名获取用户
    :param db: 数据库会话
    :param username: 用户名
    :return: 用户对象或None
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    根据邮箱获取用户
    :param db: 数据库会话
    :param email: 邮箱
    :return: 用户对象或None
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    根据ID获取用户
    :param db: 数据库会话
    :param user_id: 用户ID
    :return: 用户对象或None
    """
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户身份
    :param db: 数据库会话
    :param username: 用户名或邮箱
    :param password: 密码
    :return: 验证成功返回用户对象，失败返回None
    """
    # 尝试用户名登录
    user = get_user_by_username(db, username)

    # 如果用户名不存在，尝试邮箱登录
    if not user:
        user = get_user_by_email(db, username)

    # 验证密码（明文比较）
    if not user or user.password != password:
        return None

    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    创建新用户
    :param db: 数据库会话
    :param user_data: 用户创建数据
    :return: 创建的用户对象
    """
    # 创建用户对象
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password=user_data.password,  # 明文存储
        is_active=1
    )

    # 保存到数据库
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """
    更新用户信息
    :param db: 数据库会话
    :param user_id: 用户ID
    :param user_data: 更新数据
    :return: 更新后的用户对象或None
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    # 更新字段
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.password is not None:
        user.password = user_data.password  # 明文存储

    user.updated_at = datetime.now()

    # 保存到数据库
    db.commit()
    db.refresh(user)

    return user


def update_user_avatar(db: Session, user_id: int, avatar_url: str) -> Optional[User]:
    """
    更新用户头像
    :param db: 数据库会话
    :param user_id: 用户ID
    :param avatar_url: 头像URL
    :return: 更新后的用户对象或None
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.avatar = avatar_url
    user.updated_at = datetime.now()

    db.commit()
    db.refresh(user)

    return user
