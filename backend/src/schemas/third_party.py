"""
第三方查询相关Pydantic模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional

class DrugSearchResult(BaseModel):
    """外部药物数据库搜索结果模式"""
    external_drug_id: str = Field(..., description="外部数据库药物ID")
    name: str = Field(..., description="药物名称")
    generic_name: Optional[str] = Field(None, description="通用名")
    trade_name: Optional[str] = Field(None, description="商品名")
    manufacturer: Optional[str] = Field(None, description="生产厂家")
    specification: Optional[str] = Field(None, description="包装规格")
    dosage_form: Optional[str] = Field(None, description="产品剂型")
    is_prescription: int = Field(..., description="是否为处方药：1-处方药，0-非处方药")
    drug_image_url: Optional[str] = Field(None, description="药品图片URL")
    drug_code: Optional[str] = Field(None, description="药品编码")
    approval_number: Optional[str] = Field(None, description="批准文号")


class DrugDetailResponse(BaseModel):
    """外部药物数据库详细信息响应模式"""
    external_drug_id: str = Field(..., description="外部数据库药物ID")
    name: str = Field(..., description="药物名称")
    generic_name: Optional[str] = Field(None, description="通用名")
    trade_name: Optional[str] = Field(None, description="商品名")
    manufacturer: Optional[str] = Field(None, description="生产厂家")
    specification: Optional[str] = Field(None, description="包装规格")
    dosage_form: Optional[str] = Field(None, description="产品剂型")
    is_prescription: int = Field(..., description="是否为处方药")
    drug_image_url: Optional[str] = Field(None, description="药品图片URL")
    drug_code: Optional[str] = Field(None, description="药品编码")
    approval_number: Optional[str] = Field(None, description="批准文号")
    instruction_manual: Optional[dict] = Field(None, description="说明书内容（非处方药）")

