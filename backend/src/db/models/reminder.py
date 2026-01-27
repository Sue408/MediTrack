"""
用药提醒数据表定义
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Time
from datetime import datetime
from ..database import Base


class Reminder(Base):
    """用药提醒模型类"""
    __tablename__ = 'reminder'

    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="提醒ID")

    # 用户ID（外键）
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, comment="用户ID")

    # 药物ID（外键）
    medication_id = Column(Integer, ForeignKey('medication.id'), nullable=False, index=True, comment="药物ID")

    # 提醒时间（时:分）
    reminder_time = Column(Time, nullable=False, comment="提醒时间")

    # 星期几（JSON数组格式，如 "[1,2,3,4,5]" 表示周一到周五）
    weekdays = Column(String(50), nullable=False, comment="星期几（JSON数组）")

    # 是否启用
    is_active = Column(Integer, default=1, comment="是否启用：1-启用，0-禁用")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 更新时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 创建索引以优化查询性能
    __table_args__ = (
        Index('idx_medication_id', 'medication_id'),
    )

    def __repr__(self):
        return f"<Reminder(id={self.id}, medication_id={self.medication_id}, time={self.reminder_time})>"
