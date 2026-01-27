"""
药物相关的 Pydantic 模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import date, datetime


class MedicationBase(BaseModel):
    """药物基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="药物名称")
    dosage: Optional[str] = Field(None, max_length=50, description="剂量（如500mg）")
    frequency_type: Literal["daily", "weekly"] = Field(..., description="频率类型：daily-每日，weekly-每周")
    times_per_day: Optional[int] = Field(None, ge=1, le=10, description="每日服用次数（仅daily类型）")
    daily_times: Optional[List[str]] = Field(None, description="每日具体服用时间（HH:MM格式，仅daily类型）")
    weekly_days: Optional[List[int]] = Field(None, description="每周服用的星期几（1-7，仅weekly类型）")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    notes: Optional[str] = Field(None, description="备注")
    photos: Optional[str] = Field(None, description="药品照片JSON数组")
    barcode: Optional[str] = Field(None, max_length=100, description="药品条形码")

    @field_validator('daily_times')
    def validate_daily_times(cls, v, info):
        """验证每日服用时间格式"""
        if v is not None:
            for time_str in v:
                try:
                    hour, minute = map(int, time_str.split(':'))
                    if not (0 <= hour <= 23 and 0 <= minute <= 59):
                        raise ValueError(f"时间格式错误: {time_str}")
                except:
                    raise ValueError(f"时间格式必须为HH:MM: {time_str}")
        return v

    @field_validator('weekly_days')
    def validate_weekly_days(cls, v):
        """验证星期几"""
        if v is not None:
            if not all(1 <= day <= 7 for day in v):
                raise ValueError("星期几必须在1-7之间")
        return v


class MedicationCreate(MedicationBase):
    """药物创建请求模式"""
    pass


class MedicationUpdate(BaseModel):
    """药物更新请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="药物名称")
    dosage: Optional[str] = Field(None, max_length=50, description="剂量")
    frequency_type: Optional[Literal["daily", "weekly"]] = Field(None, description="频率类型")
    times_per_day: Optional[int] = Field(None, ge=1, le=10, description="每日服用次数")
    daily_times: Optional[List[str]] = Field(None, description="每日具体服用时间")
    weekly_days: Optional[List[int]] = Field(None, description="每周服用的星期几")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    notes: Optional[str] = Field(None, description="备注")
    photos: Optional[str] = Field(None, description="药品照片")
    barcode: Optional[str] = Field(None, max_length=100, description="条形码")
    is_active: Optional[int] = Field(None, description="是否激活：1-激活，0-停用")


class MedicationResponse(BaseModel):
    """药物信息响应模式"""
    id: int = Field(..., description="药物ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="药物名称")
    dosage: Optional[str] = Field(None, description="剂量")
    frequency_type: str = Field(..., description="频率类型")
    times_per_day: Optional[int] = Field(None, description="每日服用次数")
    daily_times: Optional[List[str]] = Field(None, description="每日具体服用时间")
    weekly_days: Optional[List[int]] = Field(None, description="每周服用的星期几")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    notes: Optional[str] = Field(None, description="备注")
    photos: Optional[str] = Field(None, description="药品照片")
    barcode: Optional[str] = Field(None, description="条形码")
    is_active: int = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True  # 允许从ORM模型创建
