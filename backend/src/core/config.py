"""
配置模块，读取环境配置
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """配置类"""
    # 服务器配置
    HOST: str = '127.0.0.1'
    PORT: int = 8000

    # Supabase配置
    SUPABASE_URL: str = None
    SUPABASE_KEY: str = None
    SUPABASE_SERVICE_KEY: str = None
    SUPABASE_JWT_SECRET: str = None

    # 数据库配置
    DATABASE_URL: str = None

    # 极速API配置（药品数据库）
    JISU_API_KEY: str = None
    JISU_API_BASE_URL: str = "https://api.jisuapi.com"

    model_config = SettingsConfigDict(env_file='.env', extra='allow')

# 定义唯一的配置实例
config = Config()