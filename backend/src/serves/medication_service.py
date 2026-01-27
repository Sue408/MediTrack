"""
药物业务逻辑层
处理药物相关的业务逻辑
"""
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
import json
from ..db.models.medication import Medication
from ..schemas.medication import MedicationCreate, MedicationUpdate


def create_medication(db: Session, user_id: int, medication_data: MedicationCreate) -> Medication:
    """
    创建新药物记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :param medication_data: 药物创建数据
    :return: 创建的药物对象
    """
    # 处理JSON字段
    daily_times_json = None
    weekly_days_json = None

    if medication_data.frequency_type == "daily" and medication_data.daily_times:
        daily_times_json = json.dumps(medication_data.daily_times)
    elif medication_data.frequency_type == "weekly" and medication_data.weekly_days:
        weekly_days_json = json.dumps(medication_data.weekly_days)

    # 创建药物对象
    db_medication = Medication(
        user_id=user_id,
        name=medication_data.name,
        dosage=medication_data.dosage,
        frequency_type=medication_data.frequency_type,
        times_per_day=medication_data.times_per_day,
        daily_times=daily_times_json,
        weekly_days=weekly_days_json,
        start_date=medication_data.start_date,
        end_date=medication_data.end_date,
        notes=medication_data.notes,
        photos=medication_data.photos,
        barcode=medication_data.barcode,
        is_active=1
    )

    # 保存到数据库
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)

    return db_medication


def get_user_medications(db: Session, user_id: int) -> List[Medication]:
    """
    获取用户的所有药物记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :return: 药物列表
    """
    return db.query(Medication).filter(Medication.user_id == user_id).all() # noqa


def get_medication_by_id(db: Session, medication_id: int, user_id: int) -> Optional[Medication]:
    """
    获取指定药物记录（验证所有权）
    :param db: 数据库会话
    :param medication_id: 药物ID
    :param user_id: 用户ID
    :return: 药物对象或None
    """
    return db.query(Medication).filter(
        Medication.id == medication_id,
        Medication.user_id == user_id
    ).first()


def update_medication(
    db: Session,
    medication_id: int,
    user_id: int,
    medication_data: MedicationUpdate
) -> Optional[Medication]:
    """
    更新药物记录
    :param db: 数据库会话
    :param medication_id: 药物ID
    :param user_id: 用户ID
    :param medication_data: 更新数据
    :return: 更新后的药物对象或None
    """
    medication = get_medication_by_id(db, medication_id, user_id)
    if not medication:
        return None

    # 更新字段（只更新提供的字段）
    if medication_data.name is not None:
        medication.name = medication_data.name
    if medication_data.dosage is not None:
        medication.dosage = medication_data.dosage
    if medication_data.frequency_type is not None:
        medication.frequency_type = medication_data.frequency_type
    if medication_data.times_per_day is not None:
        medication.times_per_day = medication_data.times_per_day
    if medication_data.daily_times is not None:
        medication.daily_times = json.dumps(medication_data.daily_times)
    if medication_data.weekly_days is not None:
        medication.weekly_days = json.dumps(medication_data.weekly_days)
    if medication_data.start_date is not None:
        medication.start_date = medication_data.start_date
    if medication_data.end_date is not None:
        medication.end_date = medication_data.end_date
    if medication_data.notes is not None:
        medication.notes = medication_data.notes
    if medication_data.barcode is not None:
        medication.barcode = medication_data.barcode
    if medication_data.is_active is not None:
        medication.is_active = medication_data.is_active
    medication.photos = medication_data.photos

    medication.updated_at = datetime.now(timezone.utc)

    # 保存到数据库
    db.commit()
    db.refresh(medication)

    return medication


def delete_medication(db: Session, medication_id: int, user_id: int) -> bool:
    """
    删除药物记录
    :param db: 数据库会话
    :param medication_id: 药物ID
    :param user_id: 用户ID
    :return: 删除成功返回True，失败返回False
    """
    medication = get_medication_by_id(db, medication_id, user_id)
    if not medication:
        return False

    db.delete(medication)
    db.commit()

    return True
