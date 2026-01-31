"""
外部药物数据库服务层
提供药物搜索和详情查询功能（对接极速API）
"""
from typing import List, Optional, Literal
import httpx
from src.core.config import config


# 极速API图片基础URL
JISU_IMAGE_BASE_URL = "https://jisuapi.com/medicine/static/images/"


async def search_drugs_from_third_party(
        query: str,
        search_type: Literal["name", "barcode", "manufacturer"] = "name",
        limit: int = 10
) -> List[dict]:
    """
    搜索药物
    :param query: 搜索关键词
    :param search_type: 搜索类型（name-名称, barcode-条码, manufacturer-厂家）
    :param limit: 返回结果数量限制
    :return: 药物列表
    """
    if not query or not query.strip():
        return []

    if not config.JISU_API_KEY:
        raise ValueError("JISU_API_KEY 未配置，请在 .env 文件中设置")

    query = query.strip()

    # 构建请求参数
    params = {
        "appkey": config.JISU_API_KEY
    }

    # 根据搜索类型设置参数
    if search_type == "name":
        params["name"] = query
    elif search_type == "barcode":
        params["barcode"] = query
    elif search_type == "manufacturer":
        params["manufacturer"] = query

    # 调用极速API
    url = f"{config.JISU_API_BASE_URL}/medicine/query"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # 检查API返回状态
            if data.get("status") != 0:
                # 如果是未找到结果，返回空数组而不是抛出异常
                error_msg = data.get('msg', '').lower()
                if 'not found' in error_msg or '未找到' in error_msg or data.get("status") == 205:
                    return []
                raise Exception(f"API错误: {data.get('msg', '未知错误')}")

            # 解析返回结果
            result_list = data.get("result", {}).get("list", [])

            # 转换为统一格式
            results = []
            for item in result_list[:limit]:
                result = {
                    "external_drug_id": f"jisu_{item['medicine_id']}",  # 添加前缀标识来源
                    "name": item["name"],
                    "generic_name": item["name"],  # API未提供通用名，使用药品名称
                    "trade_name": item["name"],  # API未提供商品名，使用药品名称
                    "manufacturer": item["manufacturer"],
                    "specification": None,  # 查询接口不返回规格，需要调用详情接口
                    "dosage_form": None,  # 查询接口不返回剂型，需要调用详情接口
                    "is_prescription": item["prescription"] == 1,  # 1=处方药, 2=OTC
                    "drug_image_url": _build_image_url(item.get("image", "")),
                    "drug_code": None,  # 查询接口不返回药品本位码
                    "approval_number": None,  # 查询接口不返回批准文号
                    "medicine_id": item["medicine_id"]  # 保留原始ID用于详情查询
                }
                results.append(result)

            return results

    except httpx.HTTPError as e:
        raise Exception(f"HTTP请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"搜索药品失败: {str(e)}")


async def get_drug_detail_from_third_party(external_drug_id: str) -> Optional[dict]:
    """
    获取药物详细信息
    :param external_drug_id: 外部数据库药物ID（格式：jisu_123 或直接传入 medicine_id）
    :return: 药物详细信息或None
    """
    if not config.JISU_API_KEY:
        raise ValueError("JISU_API_KEY 未配置，请在 .env 文件中设置")

    # 提取 medicine_id
    medicine_id = external_drug_id
    if external_drug_id.startswith("jisu_"):
        medicine_id = external_drug_id.replace("jisu_", "")

    # 构建请求参数
    params = {
        "appkey": config.JISU_API_KEY,
        "medicine_id": medicine_id
    }

    # 调用极速API
    url = f"{config.JISU_API_BASE_URL}/medicine/detail"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # 检查API返回状态
            if data.get("status") != 0:
                # 如果是未找到，返回None
                if "not found" in data.get("msg", "").lower():
                    return None
                raise Exception(f"API错误: {data.get('msg', '未知错误')}")

            # 解析返回结果
            result = data.get("result", {})

            if not result:
                return None

            # 转换为统一格式
            drug_detail = {
                "external_drug_id": f"jisu_{result['medicine_id']}",
                "name": result["name"],
                "generic_name": result["name"],  # API未单独提供通用名
                "trade_name": result["name"],  # API未单独提供商品名
                "manufacturer": result["manufacturer"],
                "specification": result.get("spec", ""),
                "dosage_form": result.get("type", ""),
                "is_prescription": result["prescription"] == 1,  # 1=处方药, 2=OTC
                "drug_image_url": _build_image_url(result.get("image", "")),
                "drug_code": result.get("reference_code", ""),  # 药品本位码
                "approval_number": result.get("approval_num", ""),
                "barcode": result.get("barcode", ""),
                "instruction_manual": _parse_instruction_manual(result) if result["prescription"] == 2 else None
            }

            return drug_detail

    except httpx.HTTPError as e:
        raise Exception(f"HTTP请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"获取药品详情失败: {str(e)}")


async def get_instruction_manual_from_third_party(external_drug_id: str) -> Optional[dict]:
    """
    获取药物说明书
    :param external_drug_id: 外部数据库药物ID
    :return: 说明书内容或None（处方药返回None）
    """
    drug = await get_drug_detail_from_third_party(external_drug_id)

    if not drug:
        return None

    # 处方药不提供说明书
    if drug["is_prescription"]:
        return None

    return drug.get("instruction_manual")


def _build_image_url(image_path: str) -> str:
    """
    构建完整的图片URL

    Args:
        image_path: API返回的图片相对路径

    Returns:
        完整的图片URL，如果没有图片返回空字符串
    """
    if not image_path:
        return ""

    # 如果已经是完整URL，直接返回
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path

    # 拼接完整URL
    return f"{JISU_IMAGE_BASE_URL}{image_path}"


def _parse_instruction_manual(result: dict) -> Optional[dict]:
    """
    解析药品说明书
    极速API返回的desc字段包含完整说明书文本，需要解析

    Args:
        result: API返回的药品详情

    Returns:
        结构化的说明书内容
    """
    desc = result.get("desc", "")
    if not desc:
        return None

    # 简单解析说明书文本
    # 极速API的desc字段格式类似：
    # 【警示】处方药须凭处方在药师指导下购买和使用！
    # 【产品名称】尼可地尔片
    # 【商品名/商标】仁彤
    # ...

    manual = {
        "适应症": result.get("disease", ""),
        "说明书全文": desc
    }

    # 尝试从desc中提取更多信息（简单实现）
    if "【适应症】" in desc or "【功能主治】" in desc:
        # 可以进一步解析，这里先返回基本信息
        pass

    return manual
