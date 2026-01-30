from ..core import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 连接PostgreSQL数据库并创建ORM基类
engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=True,  # 连接池预检查
    pool_size=5,  # 连接池大小（降低以适配Supabase连接池限制）
    max_overflow=10  # 最大溢出连接数（降低以避免连接耗尽）
)
Base = declarative_base()

# 定义数据库会话工厂函数
sessions = sessionmaker(bind=engine)

def get_db():
    """获取数据库会话"""
    db = sessions()
    try:
        yield db
    finally:
        db.close()

# 定义数据库初始化方法
def init_db():
    """数据库初始化方法"""
    from .models import UserProfile, Medication, Reminder # noqa
    Base.metadata.create_all(bind=engine)