"""
配置模块，读取环境配置
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """配置类"""
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    DATA_URL: str = 'sqlite:///data.db'
    SECRET_KEY: str = 'your-secret-key-please-change-in-production-environment'

    model_config = SettingsConfigDict(env_file='.env', extra='allow')

# 定义唯一的配置实例
config = Config()