"""
用药提醒API路由层
管理用药记录的生成、查询和完成状态
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta

from ..db.database import get_db
from ..schemas.user import UserResponse
from ..schemas.medication_record import (
    MedicationRecordResponse,
    GenerateRecordsRequest
)
from ..serves import medication_record_service
from .user import get_current_user

# 创建路由器
router = APIRouter(prefix="/reminder", tags=["用药提醒"])


@router.post("/generate")
async def generate_records(
    request: GenerateRecordsRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    生成未来N天的用药记录
    :param request: 生成请求（包含天数）
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 生成的记录数量
    """
    count = medication_record_service.generate_records_for_user(
        db, current_user.id, request.days
    )
    return {
        "message": f"成功生成 {count} 条用药记录",
        "count": count
    }


@router.get("/records")
async def get_records_by_date(
    target_date: Optional[date] = Query(None, description="目标日期，默认为今天"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取指定日期的用药记录
    :param target_date: 目标日期
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 用药记录列表
    """
    if target_date is None:
        target_date = date.today()

    records = medication_record_service.get_records_by_date(
        db, current_user.id, target_date
    )
    return records


@router.get("/records/range")
async def get_records_by_range(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取日期范围内的用药记录
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 用药记录列表
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="结束日期不能早于开始日期"
        )

    records = medication_record_service.get_date_range_records(
        db, current_user.id, start_date, end_date
    )
    return records


@router.put("/records/{record_id}/complete")
async def complete_record(
    record_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    标记用药记录为已完成
    :param record_id: 记录ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的记录
    """
    record = medication_record_service.complete_record(db, record_id, current_user.id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药记录不存在"
        )

    # 获取药物信息
    from ..db.models.medication import Medication
    medication = db.query(Medication).filter(Medication.id == record.medication_id).first()

    return {
        "id": record.id,
        "user_id": record.user_id,
        "medication_id": record.medication_id,
        "medication_name": medication.name if medication else "",
        "dosage": medication.dosage if medication else None,
        "scheduled_date": record.scheduled_date,
        "scheduled_time": record.scheduled_time,
        "is_completed": record.is_completed,
        "completed_at": record.completed_at,
        "created_at": record.created_at,
        "updated_at": record.updated_at
    }


@router.put("/records/{record_id}/uncomplete")
async def uncomplete_record(
    record_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    取消用药记录的完成状态
    :param record_id: 记录ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的记录
    """
    record = medication_record_service.uncomplete_record(db, record_id, current_user.id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药记录不存在"
        )

    # 获取药物信息
    from ..db.models.medication import Medication
    medication = db.query(Medication).filter(Medication.id == record.medication_id).first()

    return {
        "id": record.id,
        "user_id": record.user_id,
        "medication_id": record.medication_id,
        "medication_name": medication.name if medication else "",
        "dosage": medication.dosage if medication else None,
        "scheduled_date": record.scheduled_date,
        "scheduled_time": record.scheduled_time,
        "is_completed": record.is_completed,
        "completed_at": record.completed_at,
        "created_at": record.created_at,
        "updated_at": record.updated_at
    }

