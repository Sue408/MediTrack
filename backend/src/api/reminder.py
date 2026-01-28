"""
用药提醒API路由层
管理用药提醒的生成、查询和完成状态
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from ..db.database import get_db
from ..schemas.user import UserResponse
from ..schemas.reminder import RemindersRequest, ReminderResponse
from ..serves import reminder_service
from .user import get_current_user

# 创建路由器
router = APIRouter(prefix="/reminder", tags=["用药提醒"])


@router.post("/generate")
async def generate_records(
    request: RemindersRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    生成未来N天的用药提醒
    :param request: 生成请求（包含天数）
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 生成的记录数量
    """
    count = reminder_service.generate_reminders_for_user(
        db, current_user.id, request.days
    )
    return {
        "message": f"成功生成 {count} 条用药记录",
        "count": count
    }


@router.get("/")
async def get_records_by_date(
    target_date: Optional[date] = Query(None, description="目标日期，默认为今天"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取指定日期的用药提醒
    :param target_date: 目标日期
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 用药提醒列表
    """
    if target_date is None:
        target_date = date.today()

    reminders = reminder_service.get_reminders_by_date(
        db, current_user.id, target_date
    )
    return reminders


@router.get("/range")
async def get_reminders_by_range(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取日期范围内的用药提醒
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

    reminders = reminder_service.get_date_range_reminders(
        db, current_user.id, start_date, end_date
    )
    return reminders


@router.put("/{reminder_id}/complete", response_model=ReminderResponse)
async def complete_record(
    reminder_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    标记用药记录为已完成
    :param reminder_id: 记录ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的提醒
    """
    reminder = reminder_service.complete_reminder(db, reminder_id, current_user.id)
    # noinspection DuplicatedCode
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )

    # 获取药物信息
    from ..db.models.medication import Medication
    medication = db.query(Medication).filter(Medication.id == reminder.medication_id).first()

    return {
        "id": reminder.id,
        "user_id": reminder.user_id,
        "medication_id": reminder.medication_id,
        "medication_name": medication.name if medication else "",
        "dosage": medication.dosage if medication else None,
        "scheduled_date": reminder.scheduled_date,
        "scheduled_time": reminder.scheduled_time,
        "is_completed": reminder.is_completed,
        "completed_at": reminder.completed_at,
        "created_at": reminder.created_at,
        "updated_at": reminder.updated_at
    }


@router.put("/{reminder_id}/uncomplete", response_model=ReminderResponse)
async def uncomplete_reminder(
    reminder_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    取消用药提醒的完成状态
    :param reminder_id: 记录ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的提醒
    """
    record = reminder_service.uncomplete_reminder(db, reminder_id, current_user.id)
    # noinspection DuplicatedCode
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
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

