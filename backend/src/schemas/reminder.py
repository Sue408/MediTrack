"""
用药提醒相关的 Pydantic 模式定义
用于请求验证和响应序列化
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time, datetime


class ReminderBase(BaseModel):
    """提醒基础模式"""
    medication_id: int = Field(..., description="药物ID")
    reminder_time: time = Field(..., description="提醒时间（时:分）")
    weekdays: List[int] = Field(..., description="星期几（1-7，1表示周一）")


class ReminderCreate(ReminderBase):
    """提醒创建请求模式"""
    pass


class ReminderUpdate(BaseModel):
    """提醒更新请求模式"""
    reminder_time: Optional[time] = Field(None, description="提醒时间（时:分）")
    weekdays: Optional[List[int]] = Field(None, description="星期几（1-7，1表示周一）")
    is_active: Optional[int] = Field(None, description="是否启用：1-启用，0-禁用")


class ReminderResponse(BaseModel):
    """提醒信息响应模式"""
    id: int = Field(..., description="提醒ID")
    user_id: int = Field(..., description="用户ID")
    medication_id: int = Field(..., description="药物ID")
    medication_name: Optional[str] = Field(None, description="药物名称")
    reminder_time: time = Field(..., description="提醒时间")
    weekdays: List[int] = Field(..., description="星期几")
    is_active: int = Field(..., description="是否启用")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True  # 允许从ORM模型创建
