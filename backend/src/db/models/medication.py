"""
药物数据表定义
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Index, Boolean
from datetime import datetime
from ..database import Base


class Medication(Base):
    """药物模型类"""
    __tablename__ = 'medication'

    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="药物ID")

    # 用户ID（外键，UUID类型）
    user_id = Column(String(36), ForeignKey('user_profiles.id'), nullable=False, index=True, comment="用户ID")

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

    # ========== 外部药物数据库相关字段 ==========
    # 药品编码（国药准字号）
    drug_code = Column(String(100), nullable=True, comment="药品编码（国药准字号）")

    # 生产厂家
    manufacturer = Column(String(200), nullable=True, comment="生产厂家")

    # 包装规格（如"10mg*24片"）
    specification = Column(String(100), nullable=True, comment="包装规格")

    # 产品剂型（片剂、胶囊、注射液等）
    dosage_form = Column(String(50), nullable=True, comment="产品剂型")

    # 是否为处方药（布尔类型）
    is_prescription = Column(Boolean, default=False, comment="是否为处方药")

    # 药品官方图片URL
    drug_image_url = Column(String(500), nullable=True, comment="药品官方图片URL")

    # 说明书内容（JSON格式存储）
    instruction_manual = Column(Text, nullable=True, comment="说明书内容JSON格式")

    # 批准文号
    approval_number = Column(String(100), nullable=True, comment="批准文号")

    # 通用名
    generic_name = Column(String(200), nullable=True, comment="通用名")

    # 商品名
    trade_name = Column(String(200), nullable=True, comment="商品名")

    # 数据来源（manual-手动录入, api-外部API）
    data_source = Column(String(20), default="manual", comment="数据来源：manual-手动录入，api-外部API")

    # 外部数据库药物ID
    external_drug_id = Column(String(100), nullable=True, comment="外部数据库药物ID")

    # 是否激活（布尔类型）
    is_active = Column(Boolean, default=True, comment="是否激活")

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
