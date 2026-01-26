"""
药物相关的 Pydantic 模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class MedicationBase(BaseModel):
    """药物基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="药物名称")
    dosage: Optional[str] = Field(None, max_length=50, description="剂量（如500mg）")
    frequency: Optional[str] = Field(None, max_length=100, description="服用频率（如每日3次）")
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    notes: Optional[str] = Field(None, description="备注")
    photos: Optional[str] = Field(None, description="药品照片JSON数组")
    barcode: Optional[str] = Field(None, max_length=100, description="药品条形码")


class MedicationCreate(MedicationBase):
    """药物创建请求模式"""
    pass


class MedicationUpdate(BaseModel):
    """药物更新请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="药物名称")
    dosage: Optional[str] = Field(None, max_length=50, description="剂量（如500mg）")
    frequency: Optional[str] = Field(None, max_length=100, description="服用频率（如每日3次）")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    notes: Optional[str] = Field(None, description="备注")
    photos: Optional[str] = Field(None, description="药品照片JSON数组")
    barcode: Optional[str] = Field(None, max_length=100, description="药品条形码")
    is_active: Optional[int] = Field(None, description="是否激活：1-激活，0-停用")


class MedicationResponse(MedicationBase):
    """药物信息响应模式"""
    id: int = Field(..., description="药物ID")
    user_id: int = Field(..., description="用户ID")
    is_active: int = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True  # 允许从ORM模型创建
