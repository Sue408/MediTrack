"""
用药记录相关的 Pydantic 模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class MedicationRecordResponse(BaseModel):
    """用药记录响应模式"""
    id: int = Field(..., description="记录ID")
    user_id: int = Field(..., description="用户ID")
    medication_id: int = Field(..., description="药物ID")
    medication_name: str = Field(..., description="药物名称")
    dosage: Optional[str] = Field(None, description="剂量")
    scheduled_date: date = Field(..., description="计划服用日期")
    scheduled_time: Optional[str] = Field(None, description="计划服用时间")
    is_completed: bool = Field(..., description="是否已完成")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class MedicationRecordCreate(BaseModel):
    """用药记录创建请求模式"""
    medication_id: int = Field(..., description="药物ID")
    scheduled_date: date = Field(..., description="计划服用日期")
    scheduled_time: Optional[str] = Field(None, description="计划服用时间")


class GenerateRecordsRequest(BaseModel):
    """生成用药记录请求模式"""
    days: int = Field(default=7, ge=1, le=90, description="生成未来N天的记录（1-90天）")
