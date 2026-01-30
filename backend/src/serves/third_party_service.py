"""
外部药物数据库服务层
提供药物搜索和详情查询功能（当前为模拟数据）
"""
from typing import List, Optional, Literal

# 模拟药物数据库
MOCK_DRUG_DATABASE = [
    {
        "external_drug_id": "drug_001",
        "name": "阿莫西林胶囊",
        "generic_name": "阿莫西林",
        "trade_name": "阿莫西林胶囊",
        "manufacturer": "华北制药股份有限公司",
        "specification": "0.25g*24粒",
        "dosage_form": "胶囊剂",
        "is_prescription": False,
        "drug_image_url": "https://example.com/images/amoxicillin.jpg",
        "drug_code": "国药准字H13022378",
        "approval_number": "国药准字H13022378",
        "barcode": "6901234567890",
        "instruction_manual": {
            "适应症": "用于敏感菌所致的溶血性链球菌、肺炎链球菌、葡萄球菌或流感嗜血杆菌所致中耳炎、鼻窦炎、咽炎、扁桃体炎等上呼吸道感染。",
            "用法用量": "口服。成人一次0.5g，每6~8小时1次，一日剂量不超过4g。",
            "不良反应": "恶心、呕吐、腹泻及假膜性肠炎等胃肠道反应。",
            "禁忌": "青霉素类药物过敏者及传染性单核细胞增多症患者禁用。",
            "注意事项": "青霉素类药物可引起过敏性休克，用药前必须详细询问药物过敏史。"
        }
    },
    {
        "external_drug_id": "drug_002",
        "name": "布洛芬缓释胶囊",
        "generic_name": "布洛芬",
        "trade_name": "芬必得",
        "manufacturer": "中美天津史克制药有限公司",
        "specification": "0.3g*20粒",
        "dosage_form": "缓释胶囊",
        "is_prescription": False,
        "drug_image_url": "https://example.com/images/ibuprofen.jpg",
        "drug_code": "国药准字H10950170",
        "approval_number": "国药准字H10950170",
        "barcode": "6901234567891",
        "instruction_manual": {
            "适应症": "用于缓解轻至中度疼痛如头痛、关节痛、偏头痛、牙痛、肌肉痛、神经痛、痛经。也用于普通感冒或流行性感冒引起的发热。",
            "用法用量": "口服。成人，一次1粒，一日2次（早晚各一次）。",
            "不良反应": "少数病人可出现恶心、呕吐、胃烧灼感或轻度消化不良、胃肠道溃疡及出血、转氨酶升高、头痛、头晕、耳鸣、视力模糊、精神紧张、嗜睡、下肢水肿或体重骤增。",
            "禁忌": "对本品及其他非甾体抗炎药过敏者禁用；对阿司匹林过敏的哮喘患者禁用。",
            "注意事项": "有消化性溃疡史、胃肠道出血、心功能不全、高血压患者慎用。"
        }
    },
    {
        "external_drug_id": "drug_003",
        "name": "二甲双胍片",
        "generic_name": "盐酸二甲双胍",
        "trade_name": "格华止",
        "manufacturer": "中美上海施贵宝制药有限公司",
        "specification": "0.5g*20片",
        "dosage_form": "片剂",
        "is_prescription": True,
        "drug_image_url": "https://example.com/images/metformin.jpg",
        "drug_code": "国药准字H20023370",
        "approval_number": "国药准字H20023370",
        "barcode": "6901234567892",
        "instruction_manual": None  # 处方药不提供说明书
    },
    {
        "external_drug_id": "drug_004",
        "name": "阿托伐他汀钙片",
        "generic_name": "阿托伐他汀钙",
        "trade_name": "立普妥",
        "manufacturer": "辉瑞制药有限公司",
        "specification": "20mg*7片",
        "dosage_form": "片剂",
        "is_prescription": True,
        "drug_image_url": "https://example.com/images/atorvastatin.jpg",
        "drug_code": "国药准字H20051407",
        "approval_number": "国药准字H20051407",
        "barcode": "6901234567893",
        "instruction_manual": None  # 处方药不提供说明书
    },
    {
        "external_drug_id": "drug_005",
        "name": "维生素C片",
        "generic_name": "维生素C",
        "trade_name": "维生素C片",
        "manufacturer": "华中药业股份有限公司",
        "specification": "100mg*100片",
        "dosage_form": "片剂",
        "is_prescription": False,
        "drug_image_url": "https://example.com/images/vitamin_c.jpg",
        "drug_code": "国药准字H42022073",
        "approval_number": "国药准字H42022073",
        "barcode": "6901234567894",
        "instruction_manual": {
            "适应症": "用于预防坏血病，也可用于各种急慢性传染疾病及紫癜等的辅助治疗。",
            "用法用量": "口服。成人，一次1-2片，一日3次。",
            "不良反应": "长期过量服用可引起尿酸盐、半胱氨酸盐或草酸盐结石。",
            "禁忌": "尚不明确。",
            "注意事项": "不宜长期过量服用，否则，突然停药有可能出现坏血病症状。"
        }
    },
    {
        "external_drug_id": "drug_006",
        "name": "感冒灵颗粒",
        "generic_name": "感冒灵",
        "trade_name": "999感冒灵",
        "manufacturer": "华润三九医药股份有限公司",
        "specification": "10g*9袋",
        "dosage_form": "颗粒剂",
        "is_prescription": False,
        "drug_image_url": "https://example.com/images/ganmaoling.jpg",
        "drug_code": "国药准字Z44021940",
        "approval_number": "国药准字Z44021940",
        "barcode": "6901234567895",
        "instruction_manual": {
            "适应症": "解热镇痛。用于感冒引起的头痛，发热，鼻塞，流涕，咽痛等。",
            "用法用量": "开水冲服。一次10克，一日3次。",
            "不良反应": "有时有轻度头晕、乏力、恶心、上腹不适、口干、食欲缺乏和皮疹等。",
            "禁忌": "严重肝肾功能不全者禁用。",
            "注意事项": "忌烟、酒及辛辣、生冷、油腻食物。不宜在服药期间同时服用滋补性中药。"
        }
    },
    {
        "external_drug_id": "drug_007",
        "name": "硝苯地平缓释片",
        "generic_name": "硝苯地平",
        "trade_name": "拜新同",
        "manufacturer": "拜耳医药保健有限公司",
        "specification": "30mg*7片",
        "dosage_form": "缓释片",
        "is_prescription": True,
        "drug_image_url": "https://example.com/images/nifedipine.jpg",
        "drug_code": "国药准字H20000079",
        "approval_number": "国药准字H20000079",
        "barcode": "6901234567896",
        "instruction_manual": None  # 处方药不提供说明书
    },
    {
        "external_drug_id": "drug_008",
        "name": "蒙脱石散",
        "generic_name": "蒙脱石",
        "trade_name": "思密达",
        "manufacturer": "博福-益普生（天津）制药有限公司",
        "specification": "3g*10袋",
        "dosage_form": "散剂",
        "is_prescription": False,
        "drug_image_url": "https://example.com/images/smecta.jpg",
        "drug_code": "国药准字H20000690",
        "approval_number": "国药准字H20000690",
        "barcode": "6901234567897",
        "instruction_manual": {
            "适应症": "成人及儿童急、慢性腹泻。",
            "用法用量": "口服。成人每次1袋（3g），一日3次。",
            "不良反应": "可见便秘，其发生率随剂量增加而升高，但降低剂量后即可消失。",
            "禁忌": "对本品过敏者禁用。",
            "注意事项": "如服用过量或出现严重不良反应请立即就医。"
        }
    }
]


def search_drugs_from_third_party(
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

    query = query.strip().lower()
    results = []

    for drug in MOCK_DRUG_DATABASE:
        matched = False

        if search_type == "name":
            # 按名称搜索（支持通用名、商品名、药品名称）
            if (query in drug["name"].lower() or
                    query in drug.get("generic_name", "").lower() or
                    query in drug.get("trade_name", "").lower()):
                matched = True

        elif search_type == "barcode":
            # 按条码搜索（精确匹配）
            if drug.get("barcode") == query:
                matched = True

        elif search_type == "manufacturer":
            # 按厂家搜索
            if query in drug.get("manufacturer", "").lower():
                matched = True

        if matched:
            # 构建搜索结果（不包含说明书）
            result = {
                "external_drug_id": drug["external_drug_id"],
                "name": drug["name"],
                "generic_name": drug.get("generic_name"),
                "trade_name": drug.get("trade_name"),
                "manufacturer": drug.get("manufacturer"),
                "specification": drug.get("specification"),
                "dosage_form": drug.get("dosage_form"),
                "is_prescription": drug["is_prescription"],
                "drug_image_url": drug.get("drug_image_url"),
                "drug_code": drug.get("drug_code"),
                "approval_number": drug.get("approval_number")
            }
            results.append(result)

        # 达到限制数量后停止
        if len(results) >= limit:
            break

    return results

def get_drug_detail_from_third_party(external_drug_id: str) -> Optional[dict]:
    """
    获取药物详细信息
    :param external_drug_id: 外部数据库药物ID
    :return: 药物详细信息或None
    """
    for drug in MOCK_DRUG_DATABASE:
        if drug["external_drug_id"] == external_drug_id:
            # 返回完整信息（包含说明书）
            return {
                "external_drug_id": drug["external_drug_id"],
                "name": drug["name"],
                "generic_name": drug.get("generic_name"),
                "trade_name": drug.get("trade_name"),
                "manufacturer": drug.get("manufacturer"),
                "specification": drug.get("specification"),
                "dosage_form": drug.get("dosage_form"),
                "is_prescription": drug["is_prescription"],
                "drug_image_url": drug.get("drug_image_url"),
                "drug_code": drug.get("drug_code"),
                "approval_number": drug.get("approval_number"),
                "instruction_manual": drug.get("instruction_manual")
            }

    return None

def get_instruction_manual_from_third_party(external_drug_id: str) -> Optional[dict]:
    """
    获取药物说明书
    :param external_drug_id: 外部数据库药物ID
    :return: 说明书内容或None（处方药返回None）
    """
    drug = get_drug_detail_from_third_party(external_drug_id)

    if not drug:
        return None

    # 处方药不提供说明书
    if drug["is_prescription"] == 1:
        return None

    return drug.get("instruction_manual")