import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.core import config
from src.db import init_db
from src.api import user_router, medication_router, reminder_router, third_party_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """应用生命周期管理"""
    print("开始初始化数据库...")
    init_db()  # 初始化数据库
    print("成功初始化数据库...")
    print(f"后端地址: {config.HOST}:{config.PORT}")
    yield
    print("应用关闭...")

# noinspection SpellCheckingInspection
def main():
    """程序入口函数"""
    # 初始化APP
    app = FastAPI(
        title="MediTrack API",
        description="面向患者的药物管理平台",
        version="0.1.0",
        lifespan=lifespan
    )

    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # 注册用户路由
    app.include_router(user_router)

    # 注册药物路由
    app.include_router(medication_router)

    # 注册提醒路由
    app.include_router(reminder_router)

    # 注册第三方查询路由
    app.include_router(third_party_router)

    # 启动uvicorn服务
    uvicorn.run(app, host=config.HOST, port=config.PORT)

if __name__ == "__main__":
    main()
