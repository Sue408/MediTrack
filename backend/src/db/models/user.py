"""
用户Profile数据表定义
与Supabase Auth集成，存储扩展用户信息
"""
from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from ..database import Base

class UserProfile(Base):
    """用户Profile模型类

    注意：此表与Supabase的auth.users表关联
    - id字段对应auth.users.id（UUID）
    - 认证信息（email, password）由Supabase Auth管理
    - 此表仅存储扩展信息（username, avatar_url, full_name等）
    """
    __tablename__ = 'user_profiles'

    # 主键ID（UUID，关联auth.users.id）
    id = Column(String(36), primary_key=True, index=True, comment="用户ID（UUID）")

    # 用户名（唯一）
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")

    # 头像URL（Supabase Storage）
    avatar_url = Column(Text, nullable=True, comment="头像URL")

    # 真实姓名（可选）
    full_name = Column(String(100), nullable=True, comment="真实姓名")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 更新时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, username={self.username})>"