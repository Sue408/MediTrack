"""
第三方数据库药品查询API
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Literal
from ..schemas.third_party import DrugSearchResult, DrugDetailResponse
from ..serves.third_party_service import (
    search_drugs_from_third_party,
    get_drug_detail_from_third_party,
    get_instruction_manual_from_third_party)

router = APIRouter(prefix="/third-party", tags=["第三方数据库查询服务"])


@router.get("", response_model=List[DrugSearchResult])
async def search_drugs(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    search_type: Literal["name", "barcode", "manufacturer"] = Query("name", description="搜索类型"),
    limit: int = Query(10, ge=1, le=50, description="返回结果数量限制")
):
    """
    搜索外部药物数据库
    :param query: 搜索关键词
    :param search_type: 搜索类型（name-名称, barcode-条码, manufacturer-厂家）
    :param limit: 返回结果数量限制
    :return: 药物搜索结果列表
    """
    try:
        results = await search_drugs_from_third_party(query, search_type, limit)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索药物失败: {str(e)}"
        )


@router.get("/drug-detail/{external_drug_id}", response_model=DrugDetailResponse)
async def get_drug_detail(
    external_drug_id: str
):
    """
    获取外部数据库中的药物详细信息
    :param external_drug_id: 外部数据库药物ID
    :return: 药物详细信息
    """
    drug = await get_drug_detail_from_third_party(external_drug_id)
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="药物信息不存在"
        )
    return drug


@router.get("/instruction/{external_drug_id}")
async def get_instruction_manual(
    external_drug_id: str
):
    """
    获取药物说明书
    :param external_drug_id: 外部数据库药物ID
    :return: 说明书内容（仅非处方药可访问）
    """
    instruction = await get_instruction_manual_from_third_party(external_drug_id)
    if instruction is None:
        # 检查药物是否存在
        drug = await get_drug_detail_from_third_party(external_drug_id)
        if not drug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="药物信息不存在"
            )
        # 药物存在但是处方药
        if drug["is_prescription"] == 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="处方药不提供说明书信息"
            )
        # 其他情况
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="说明书信息不存在"
        )

    return {
        "external_drug_id": external_drug_id,
        "instruction_manual": instruction
    }