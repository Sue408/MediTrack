"""
药物API路由层
处理药物相关的HTTP请求
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Any
import json
from ..db.database import get_db
from ..schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse
)
from ..schemas.user import UserResponse
from ..serves import medication_service
from .user import get_current_user

# 创建路由器
router = APIRouter(prefix="/medications", tags=["药物管理"])


def _safe_json_parse(json_str: Optional[str], default: Any = None) -> Any:
    """
    安全解析JSON字符串
    :param json_str: JSON字符串
    :param default: 解析失败时的默认值
    :return: 解析后的对象或默认值
    """
    if not json_str:
        return default
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def _build_medication_response(medication) -> MedicationResponse:
    """
    构建药物响应对象，解析JSON字段
    """
    return MedicationResponse(
        id=medication.id,
        user_id=medication.user_id,
        name=medication.name,
        dosage=medication.dosage,
        frequency_type=medication.frequency_type,
        times_per_day=medication.times_per_day,
        daily_times=_safe_json_parse(medication.daily_times, []),
        weekly_days=_safe_json_parse(medication.weekly_days, []),
        start_date=medication.start_date,
        end_date=medication.end_date,
        notes=medication.notes,
        photos=medication.photos,
        barcode=medication.barcode,
        is_active=medication.is_active,
        created_at=medication.created_at,
        updated_at=medication.updated_at,
        # 外部药物数据库相关字段
        drug_code=medication.drug_code,
        manufacturer=medication.manufacturer,
        specification=medication.specification,
        dosage_form=medication.dosage_form,
        is_prescription=medication.is_prescription,
        drug_image_url=medication.drug_image_url,
        instruction_manual=medication.instruction_manual,
        approval_number=medication.approval_number,
        generic_name=medication.generic_name,
        trade_name=medication.trade_name,
        data_source=medication.data_source,
        external_drug_id=medication.external_drug_id
    )


@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_medication(
    medication_data: MedicationCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建药物记录
    :param medication_data: 药物创建数据
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 创建的药物信息
    """
    medication = medication_service.create_medication(db, current_user.id, medication_data)
    return _build_medication_response(medication)


@router.get("", response_model=List[MedicationResponse])
async def get_medications(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有药物记录
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 药物列表
    """
    medications = medication_service.get_user_medications(db, current_user.id)
    return [_build_medication_response(med) for med in medications]


@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取指定药物记录
    :param medication_id: 药物ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 药物信息
    """
    medication = medication_service.get_medication_by_id(db, medication_id, current_user.id)
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "药物记录不存在或无权访问",
                "medication_id": medication_id,
                "error_code": "MEDICATION_NOT_FOUND",
                "suggestion": "请检查药物ID是否正确，或确认该药物属于您的账户"
            }
        )
    return _build_medication_response(medication)


@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(
    medication_id: int,
    medication_data: MedicationUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新药物记录
    :param medication_id: 药物ID
    :param medication_data: 更新数据
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 更新后的药物信息
    """
    medication = medication_service.update_medication(
        db, medication_id, current_user.id, medication_data
    )
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "无法更新药物记录",
                "medication_id": medication_id,
                "error_code": "MEDICATION_UPDATE_FAILED",
                "suggestion": "请确认药物ID正确且该药物属于您的账户"
            }
        )
    return _build_medication_response(medication)


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(
    medication_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除药物记录
    :param medication_id: 药物ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 无内容
    """
    success = medication_service.delete_medication(db, medication_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "无法删除药物记录",
                "medication_id": medication_id,
                "error_code": "MEDICATION_DELETE_FAILED",
                "suggestion": "请确认药物ID正确且该药物属于您的账户"
            }
        )