"""
Supabase集成服务层
处理Supabase Auth认证和Storage存储
"""
from typing import Optional, Dict, Any
from supabase import create_client, Client
from jose import jwt, JWTError
from ..core.config import config

# 初始化Supabase客户端
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)


def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证Supabase JWT token

    使用项目的JWT Secret验证token的签名和有效性。
    验证成功后返回token的payload，包含用户ID、邮箱等信息。

    :param token: JWT token字符串
    :return: 解码后的payload字典，验证失败返回None
    """
    try:
        # 使用Supabase项目的JWT Secret来验证token
        jwt_secret = config.SUPABASE_JWT_SECRET

        # 解码并验证token（验证签名、过期时间、audience等）
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=["HS256"],
            audience="authenticated"
        )

        return payload

    except JWTError as e:
        # JWT验证失败（签名错误、过期、audience不匹配等）
        print(f"JWT验证失败: {type(e).__name__}")
        return None
    except Exception as e:
        # 其他异常
        print(f"Token验证异常: {type(e).__name__}")
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    从JWT token中提取用户ID

    :param token: JWT token字符串
    :return: 用户ID（UUID格式），验证失败返回None
    """
    payload = verify_supabase_token(token)
    if payload:
        return payload.get("sub")
    return None


def upload_avatar(user_id: str, file_data: bytes, file_ext: str) -> Optional[str]:
    """
    上传用户头像到Supabase Storage

    文件存储路径：avatars/{user_id}/avatar.{ext}
    如果文件已存在，会被覆盖（upsert=True）

    :param user_id: 用户ID（UUID）
    :param file_data: 文件二进制数据
    :param file_ext: 文件扩展名（如jpg, png）
    :return: 头像的公开访问URL，失败返回None
    """
    try:
        # 构建文件路径：{user_id}/avatar.{ext}
        file_path = f"{user_id}/avatar.{file_ext}"

        # 上传到avatars bucket（如果文件存在则覆盖）
        supabase.storage.from_("avatars").upload(
            file_path,
            file_data,
            file_options={"content-type": f"image/{file_ext}", "upsert": "true"} # noqa
        )

        # 获取文件的公开访问URL
        public_url = supabase.storage.from_("avatars").get_public_url(file_path)

        return public_url
    except Exception as e:
        print(f"上传头像失败: {str(e)}")
        return None
