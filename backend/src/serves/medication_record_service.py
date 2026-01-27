"""
用药记录业务逻辑层
处理用药记录的生成、查询和更新
"""
from datetime import datetime, timezone, date, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
import json

from ..db.models.medication import Medication
from ..db.models.medication_record import MedicationRecord


def generate_records_for_user(db: Session, user_id: int, days: int = 7) -> int:
    """
    为用户生成未来N天的用药记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :param days: 生成天数
    :return: 生成的记录数量
    """
    # 获取用户所有激活的药物
    medications = db.query(Medication).filter(
        Medication.user_id == user_id,
        Medication.is_active == 1
    ).all()

    today = date.today()
    generated_count = 0

    for med in medications:
        # 为每一天生成记录
        for day_offset in range(days):
            target_date = today + timedelta(days=day_offset)

            # 检查是否在药物有效期内
            if target_date < med.start_date:
                continue
            if med.end_date and target_date > med.end_date:
                continue

            # 根据频率类型生成记录
            if med.frequency_type == "daily":
                # 每日类型：为每个时间点生成记录
                daily_times = []
                if med.daily_times:
                    try:
                        daily_times = json.loads(med.daily_times)
                    except:
                        pass

                for time_str in daily_times:
                    # 检查是否已存在该记录
                    existing = db.query(MedicationRecord).filter(
                        MedicationRecord.user_id == user_id,
                        MedicationRecord.medication_id == med.id,
                        MedicationRecord.scheduled_date == target_date,
                        MedicationRecord.scheduled_time == time_str
                    ).first()

                    if not existing:
                        record = MedicationRecord(
                            user_id=user_id,
                            medication_id=med.id,
                            scheduled_date=target_date,
                            scheduled_time=time_str,
                            is_completed=False
                        )
                        db.add(record)
                        generated_count += 1

            elif med.frequency_type == "weekly":
                # 每周类型：检查今天是否在服用日期中
                weekly_days = []
                if med.weekly_days:
                    try:
                        weekly_days = json.loads(med.weekly_days)
                    except:
                        pass

                target_weekday = target_date.isoweekday()  # 1=周一, 7=周日
                if target_weekday in weekly_days:
                    # 检查是否已存在该记录
                    existing = db.query(MedicationRecord).filter(
                        MedicationRecord.user_id == user_id,
                        MedicationRecord.medication_id == med.id,
                        MedicationRecord.scheduled_date == target_date
                    ).first()

                    if not existing:
                        record = MedicationRecord(
                            user_id=user_id,
                            medication_id=med.id,
                            scheduled_date=target_date,
                            scheduled_time=None,  # 每周类型没有具体时间
                            is_completed=False
                        )
                        db.add(record)
                        generated_count += 1

    db.commit()
    return generated_count


def get_records_by_date(db: Session, user_id: int, target_date: date) -> List[dict]:
    """
    获取指定日期的用药记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :param target_date: 目标日期
    :return: 用药记录列表
    """
    records = db.query(MedicationRecord, Medication).join(
        Medication, MedicationRecord.medication_id == Medication.id
    ).filter(
        MedicationRecord.user_id == user_id,
        MedicationRecord.scheduled_date == target_date
    ).order_by(
        MedicationRecord.scheduled_time.asc().nullslast()
    ).all()

    result = []
    for record, medication in records:
        result.append({
            "id": record.id,
            "user_id": record.user_id,
            "medication_id": record.medication_id,
            "medication_name": medication.name,
            "dosage": medication.dosage,
            "scheduled_date": record.scheduled_date,
            "scheduled_time": record.scheduled_time,
            "is_completed": record.is_completed,
            "completed_at": record.completed_at,
            "created_at": record.created_at,
            "updated_at": record.updated_at
        })

    return result


def complete_record(db: Session, record_id: int, user_id: int) -> Optional[MedicationRecord]:
    """
    标记用药记录为已完成
    :param db: 数据库会话
    :param record_id: 记录ID
    :param user_id: 用户ID
    :return: 更新后的记录或None
    """
    record = db.query(MedicationRecord).filter(
        MedicationRecord.id == record_id,
        MedicationRecord.user_id == user_id
    ).first()

    if not record:
        return None

    record.is_completed = True
    record.completed_at = datetime.now(timezone.utc)
    record.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(record)

    return record


def uncomplete_record(db: Session, record_id: int, user_id: int) -> Optional[MedicationRecord]:
    """
    取消用药记录的完成状态
    :param db: 数据库会话
    :param record_id: 记录ID
    :param user_id: 用户ID
    :return: 更新后的记录或None
    """
    record = db.query(MedicationRecord).filter(
        MedicationRecord.id == record_id,
        MedicationRecord.user_id == user_id
    ).first()

    if not record:
        return None

    record.is_completed = False
    record.completed_at = None
    record.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(record)

    return record


def get_date_range_records(db: Session, user_id: int, start_date: date, end_date: date) -> List[dict]:
    """
    获取日期范围内的用药记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 用药记录列表
    """
    records = db.query(MedicationRecord, Medication).join(
        Medication, MedicationRecord.medication_id == Medication.id
    ).filter(
        MedicationRecord.user_id == user_id,
        MedicationRecord.scheduled_date >= start_date,
        MedicationRecord.scheduled_date <= end_date
    ).order_by(
        MedicationRecord.scheduled_date.asc(),
        MedicationRecord.scheduled_time.asc().nullslast()
    ).all()

    result = []
    for record, medication in records:
        result.append({
            "id": record.id,
            "user_id": record.user_id,
            "medication_id": record.medication_id,
            "medication_name": medication.name,
            "dosage": medication.dosage,
            "scheduled_date": record.scheduled_date,
            "scheduled_time": record.scheduled_time,
            "is_completed": record.is_completed,
            "completed_at": record.completed_at,
            "created_at": record.created_at,
            "updated_at": record.updated_at
        })

    return result
