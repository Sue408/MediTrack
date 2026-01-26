"""
药物API路由层
处理药物相关的HTTP请求
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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
router = APIRouter(prefix="/medication", tags=["药物管理"])


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
    return MedicationResponse.model_validate(medication)


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
    return [MedicationResponse.model_validate(med) for med in medications]


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
            detail="药物记录不存在"
        )
    return MedicationResponse.model_validate(medication)


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
            detail="药物记录不存在"
        )
    return MedicationResponse.model_validate(medication)


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
            detail="药物记录不存在"
        )
