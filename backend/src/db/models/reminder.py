"""
用药提醒数据表定义
记录每次用药的计划时间和完成状态
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Index
from datetime import datetime
from ..database import Base


class Reminder(Base):
    """用药记录模型类"""
    __tablename__ = 'reminder'

    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="记录ID")

    # 用户ID（外键，UUID类型）
    user_id = Column(String(36), ForeignKey('user_profiles.id'), nullable=False, index=True, comment="用户ID")

    # 药物ID（外键）
    medication_id = Column(Integer, ForeignKey('medication.id'), nullable=False, index=True, comment="药物ID")

    # 计划日期
    scheduled_date = Column(Date, nullable=False, comment="计划服用日期")

    # 计划时间（仅daily类型有具体时间）
    scheduled_time = Column(String(5), nullable=True, comment="计划服用时间（HH:MM格式）")

    # 是否完成
    is_completed = Column(Boolean, default=False, comment="是否已完成")

    # 完成时间
    completed_at = Column(DateTime, nullable=True, comment="完成时间")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 更新时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 创建索引以优化查询性能
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'scheduled_date'),
        Index('idx_medication_date', 'medication_id', 'scheduled_date'),
    )

    def __repr__(self):
        return f"<MedicationRecord(id={self.id}, medication_id={self.medication_id}, date={self.scheduled_date})>"
