"""
用药提醒业务逻辑层
处理提醒相关的业务逻辑
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import json

from ..db.models.reminder import Reminder
from ..db.models.medication import Medication
from ..schemas.reminder import ReminderCreate, ReminderUpdate


def create_reminder(db: Session, user_id: int, reminder_data: ReminderCreate) -> Reminder:
    """
    创建用药提醒
    :param db: 数据库会话
    :param user_id: 用户ID
    :param reminder_data: 提醒创建数据
    :return: 创建的提醒对象
    """
    # 验证药物是否属于该用户
    medication = db.query(Medication).filter(
        Medication.id == reminder_data.medication_id,
        Medication.user_id == user_id
    ).first()

    if not medication:
        return None

    # 创建提醒对象
    db_reminder = Reminder(
        user_id=user_id,
        medication_id=reminder_data.medication_id,
        reminder_time=reminder_data.reminder_time,
        weekdays=json.dumps(reminder_data.weekdays),  # 转换为JSON字符串
        is_active=1
    )

    # 保存到数据库
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return db_reminder


def get_reminders_by_user(db: Session, user_id: int, is_active: Optional[int] = None) -> List[Reminder]:
    """
    获取用户的所有提醒
    :param db: 数据库会话
    :param user_id: 用户ID
    :param is_active: 是否只获取启用的提醒
    :return: 提醒列表
    """
    query = db.query(Reminder).filter(Reminder.user_id == user_id)

    if is_active is not None:
        query = query.filter(Reminder.is_active == is_active)

    return query.order_by(Reminder.reminder_time).all()


def get_reminder_by_id(db: Session, reminder_id: int, user_id: int) -> Optional[Reminder]:
    """
    根据ID获取提醒（验证所有权）
    :param db: 数据库会话
    :param reminder_id: 提醒ID
    :param user_id: 用户ID
    :return: 提醒对象或None
    """
    return db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user_id
    ).first()


def update_reminder(db: Session, reminder_id: int, user_id: int, reminder_data: ReminderUpdate) -> Optional[Reminder]:
    """
    更新提醒信息
    :param db: 数据库会话
    :param reminder_id: 提醒ID
    :param user_id: 用户ID
    :param reminder_data: 更新数据
    :return: 更新后的提醒对象或None
    """
    # 查询提醒（验证所有权）
    reminder = get_reminder_by_id(db, reminder_id, user_id)
    if not reminder:
        return None

    # 更新字段
    if reminder_data.reminder_time is not None:
        reminder.reminder_time = reminder_data.reminder_time
    if reminder_data.weekdays is not None:
        reminder.weekdays = json.dumps(reminder_data.weekdays)
    if reminder_data.is_active is not None:
        reminder.is_active = reminder_data.is_active

    reminder.updated_at = datetime.now()

    # 保存到数据库
    db.commit()
    db.refresh(reminder)

    return reminder


def delete_reminder(db: Session, reminder_id: int, user_id: int) -> bool:
    """
    删除提醒
    :param db: 数据库会话
    :param reminder_id: 提醒ID
    :param user_id: 用户ID
    :return: 是否删除成功
    """
    # 查询提醒（验证所有权）
    reminder = get_reminder_by_id(db, reminder_id, user_id)
    if not reminder:
        return False

    # 删除提醒
    db.delete(reminder)
    db.commit()

    return True


def get_reminders_by_medication(db: Session, medication_id: int, user_id: int) -> List[Reminder]:
    """
    获取指定药物的所有提醒
    :param db: 数据库会话
    :param medication_id: 药物ID
    :param user_id: 用户ID
    :return: 提醒列表
    """
    return db.query(Reminder).filter(
        Reminder.medication_id == medication_id,
        Reminder.user_id == user_id
    ).order_by(Reminder.reminder_time).all()
