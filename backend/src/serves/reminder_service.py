"""
用药提醒业务逻辑层
处理用药提醒的生成、查询和更新
"""
from datetime import datetime, date, timedelta
from typing import List
from sqlalchemy.orm import Session
from typing import Any
import json
from ..db.models.medication import Medication
from ..db.models.reminder import Reminder


def generate_reminders_for_user(db: Session, user_id: int, days: int = 7) -> int:
    """
    为用户生成未来N天的用药提醒
    :param db: 数据库会话
    :param user_id: 用户ID
    :param days: 生成天数
    :return: 生成的记录数量
    """
    # 获取用户所有激活的药物
    medications:List[Any] = db.query(Medication).filter(
        Medication.user_id == user_id,
        Medication.is_active == 1
    ).all()

    today = date.today() # 获取当前时间
    generated_count = 0 # 初始化记录数量

    for med in medications:
        # 为每一天生成记录
        for day_offset in range(days):
            target_date = today + timedelta(days=day_offset)

            # 检查是否在药物有效期内
            if target_date < med.start_date or target_date > med.end_date:
                continue

            # 根据频率类型生成记录
            if med.frequency_type == "daily":
                # 每日类型：为每个时间点生成记录
                daily_times = []
                if med.daily_times:
                    try:
                        daily_times = json.loads(med.daily_times) # noqa
                    except: # noqa
                        pass

                for time_str in daily_times:
                    # 检查是否已存在该记录
                    existing = db.query(Reminder).filter(
                        Reminder.user_id == user_id,
                        Reminder.medication_id == med.id,
                        Reminder.scheduled_date == target_date,
                        Reminder.scheduled_time == time_str
                    ).first()

                    # 如果存在则添加相关记录
                    if not existing:
                        reminder = Reminder(
                            user_id=user_id,
                            medication_id=med.id,
                            scheduled_date=target_date,
                            scheduled_time=time_str,
                            is_completed=False
                        )
                        db.add(reminder)
                        generated_count += 1

            elif med.frequency_type == "weekly":
                # 每周类型：检查今天是否在服用日期中
                weekly_days = []
                if med.weekly_days:
                    try:
                        weekly_days = json.loads(med.weekly_days)
                    except: # noqa
                        pass

                target_weekday = target_date.isoweekday()  # 1=周一, 7=周日
                if target_weekday in weekly_days:
                    # 检查是否已存在该记录
                    existing = db.query(Reminder).filter(
                        Reminder.user_id == user_id,
                        Reminder.medication_id == med.id,
                        Reminder.scheduled_date == target_date
                    ).first()

                    if not existing:
                        record = Reminder(
                            user_id=user_id,
                            medication_id=med.id,
                            scheduled_date=target_date,
                            scheduled_time=None,  # 每周类型没有具体时间 # noqa
                            is_completed=False
                        )
                        db.add(record)
                        generated_count += 1

    db.commit()
    return generated_count


def get_reminders_by_date(db: Session, user_id: int, target_date: date) -> List[dict]:
    """
    获取指定日期的用药提醒
    :param db: 数据库会话
    :param user_id: 用户ID
    :param target_date: 目标日期
    :return: 用药记录列表
    """
    # 获取查询记录 [(药物记录, 药物数据)] (nulls last-空值排在前面)
    reminders = db.query(Reminder, Medication).join(
        Medication, Reminder.medication_id == Medication.id
    ).filter(
        Reminder.user_id == user_id,
        Reminder.scheduled_date == target_date
    ).order_by(
        Reminder.scheduled_time.asc().nullslast()
    ).all()

    # noinspection DuplicatedCode
    result = []
    for reminder, medication in reminders:
        result.append({
            "id": reminder.id,
            "user_id": reminder.user_id,
            "medication_id": reminder.medication_id,
            "medication_name": medication.name,
            "dosage": medication.dosage,
            "scheduled_date": reminder.scheduled_date,
            "scheduled_time": reminder.scheduled_time,
            "is_completed": reminder.is_completed,
            "completed_at": reminder.completed_at,
            "created_at": reminder.created_at,
            "updated_at": reminder.updated_at
        })

    return result


def complete_reminder(db: Session, reminder_id: int, user_id: int) -> type[Reminder] | None:
    """
    标记用药提醒为已完成
    :param db: 数据库会话
    :param reminder_id: 记录ID
    :param user_id: 用户ID
    :return: 更新后的记录或None
    """
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user_id
    ).first()

    if not reminder:
        return None

    reminder.is_completed = True
    reminder.completed_at = datetime.now()
    reminder.updated_at = datetime.now()

    db.commit()
    db.refresh(reminder)

    return reminder


def uncomplete_reminder(db: Session, reminder_id: int, user_id: int) -> type[Reminder] | None:
    """
    取消用药记录的完成状态
    :param db: 数据库会话
    :param reminder_id: 记录ID
    :param user_id: 用户ID
    :return: 更新后的记录或None
    """
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user_id
    ).first()

    if not reminder:
        return None

    reminder.is_completed = False
    reminder.completed_at = None
    reminder.updated_at = datetime.now()

    db.commit()
    db.refresh(reminder)

    return reminder


def get_date_range_reminders(db: Session, user_id: int, start_date: date, end_date: date) -> List[dict]:
    """
    获取日期范围内的用药记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 用药记录列表
    """
    reminders = db.query(Reminder, Medication).join(
        Medication, Reminder.medication_id == Medication.id
    ).filter(
        Reminder.user_id == user_id,
        Reminder.scheduled_date >= start_date,
        Reminder.scheduled_date <= end_date
    ).order_by(
        Reminder.scheduled_date.asc(),
        Reminder.scheduled_time.asc().nullslast()
    ).all()

    # noinspection DuplicatedCode
    result = []
    for reminder, medication in reminders:
        result.append({
            "id": reminder.id,
            "user_id": reminder.user_id,
            "medication_id": reminder.medication_id,
            "medication_name": medication.name,
            "dosage": medication.dosage,
            "scheduled_date": reminder.scheduled_date,
            "scheduled_time": reminder.scheduled_time,
            "is_completed": reminder.is_completed,
            "completed_at": reminder.completed_at,
            "created_at": reminder.created_at,
            "updated_at": reminder.updated_at
        })

    return result
