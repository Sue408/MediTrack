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


def create_medication(db: Session, user_id: str, medication_data: MedicationCreate) -> Medication:
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
        # 外部药物数据库相关字段
        drug_code=medication_data.drug_code,
        manufacturer=medication_data.manufacturer,
        specification=medication_data.specification,
        dosage_form=medication_data.dosage_form,
        is_prescription=medication_data.is_prescription,
        drug_image_url=medication_data.drug_image_url,
        instruction_manual=medication_data.instruction_manual,
        approval_number=medication_data.approval_number,
        generic_name=medication_data.generic_name,
        trade_name=medication_data.trade_name,
        data_source=medication_data.data_source or "manual",
        external_drug_id=medication_data.external_drug_id
    )

    # 保存到数据库
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)

    return db_medication


def get_user_medications(db: Session, user_id: str) -> List[Medication]:
    """
    获取用户的所有药物记录
    :param db: 数据库会话
    :param user_id: 用户ID
    :return: 药物列表
    """
    return db.query(Medication).filter(Medication.user_id == user_id).all() # noqa


def get_medication_by_id(db: Session, medication_id: int, user_id: str) -> Optional[Medication]:
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
    user_id: str,
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

    # 只获取实际提供的字段（排除未设置的字段）
    update_dict = medication_data.model_dump(exclude_unset=True)

    # 处理需要JSON序列化的字段
    if 'daily_times' in update_dict and update_dict['daily_times'] is not None:
        update_dict['daily_times'] = json.dumps(update_dict['daily_times'])
    if 'weekly_days' in update_dict and update_dict['weekly_days'] is not None:
        update_dict['weekly_days'] = json.dumps(update_dict['weekly_days'])

    # 批量更新所有字段
    for key, value in update_dict.items():
        setattr(medication, key, value)

    # 更新时间戳
    medication.updated_at = datetime.now(timezone.utc)

    # 保存到数据库
    db.commit()
    db.refresh(medication)

    return medication


def delete_medication(db: Session, medication_id: int, user_id: str) -> bool:
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
