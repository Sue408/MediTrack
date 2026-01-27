"""
药物数据表定义
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Index
from datetime import datetime
from ..database import Base


class Medication(Base):
    """药物模型类"""
    __tablename__ = 'medication'

    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="药物ID")

    # 用户ID（外键）
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, comment="用户ID")

    # 药物名称
    name = Column(String(100), nullable=False, comment="药物名称")

    # 剂量
    dosage = Column(String(50), nullable=True, comment="剂量（如500mg）")

    # 服用频率类型（daily-每日, weekly-每周）
    frequency_type = Column(String(20), nullable=False, comment="频率类型：daily-每日，weekly-每周")

    # 每日服用次数（仅当frequency_type=daily时有效）
    times_per_day = Column(Integer, nullable=True, comment="每日服用次数")

    # 具体服用时间（JSON数组，如 ["08:00", "12:00", "18:00"]，仅当frequency_type=daily时有效）
    daily_times = Column(Text, nullable=True, comment="每日具体服用时间JSON数组")

    # 每周服用的星期几（JSON数组，如 [1, 3, 5] 表示周一、周三、周五，仅当frequency_type=weekly时有效）
    weekly_days = Column(Text, nullable=True, comment="每周服用的星期几JSON数组")

    # 开始日期
    start_date = Column(Date, nullable=False, comment="开始日期")

    # 结束日期
    end_date = Column(Date, nullable=True, comment="结束日期")

    # 备注
    notes = Column(Text, nullable=True, comment="备注")

    # 药品照片（JSON数组格式存储多张照片的Base64）
    photos = Column(Text, nullable=True, comment="药品照片JSON数组")

    # 条形码
    barcode = Column(String(100), nullable=True, comment="药品条形码")

    # 是否激活
    is_active = Column(Integer, default=1, comment="是否激活：1-激活，0-停用")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 更新时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 创建索引以优化查询性能
    __table_args__ = (
        Index('idx_user_id_is_active', 'user_id', 'is_active'),
    )

    def __repr__(self):
        return f"<Medication(id={self.id}, name={self.name}, user_id={self.user_id})>"
