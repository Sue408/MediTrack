from ..core import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 连接数据库并创建ORM基类
engine = create_engine(f'{config.DATA_URL}')
Base = declarative_base()

# 定义数据库对话工厂函数
sessions = sessionmaker(bind=engine)
def get_db():
    """获取数据库对话"""
    db = sessions()
    try:
        yield db
    finally:
        db.close()

# 定义数据库初始化方法
def init_db():
    """数据库初始化方法"""
    from .models import User
    Base.metadata.create_all(bind=engine)