"""
用户数据表定义
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from ..database import Base

class User(Base):
    """用户模型类"""
    # noinspection SpellCheckingInspection
    __tablename__ = 'user'

    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="用户ID")

    # 用户名（唯一）
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")

    # 邮箱（唯一）
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")

    # 密码（明文存储）
    password = Column(String(50), nullable=False, comment="密码")

    # 头像Base64编码（可选）
    avatar = Column(Text, nullable=True, comment="头像Base64编码")

    # 真实姓名（可选）
    full_name = Column(String(100), nullable=True, comment="真实姓名")

    # 账户状态（是否激活）
    is_active = Column(Integer, default=1, comment="账户状态：1-激活，0-禁用")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 更新时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"