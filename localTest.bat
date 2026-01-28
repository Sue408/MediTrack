@echo off
chcp 65001 >nul
echo 切换到本地开发环境...
echo.

cd /d "%~dp0frontend"
if not exist .env.local.template (
    echo 错误: 找不到 .env.local.template 文件
    echo 正在创建默认配置...
    (
        echo # 本地开发环境配置
        echo VITE_HOST=127.0.0.1
        echo VITE_PORT=5173
        echo VITE_API_BASE_URL=/api
        echo VITE_PROXY_TARGET=http://localhost:8000
    ) > .env.local
) else (
    copy /Y .env.local.template .env.local >nul
)

echo 已切换到本地开发环境
echo.
echo 配置信息:
echo   - 前端地址: http://localhost:5173
echo   - 后端地址: http://localhost:8000
echo   - API 路径: /api (通过 Vite 代理)
echo.
echo 启动方式:
echo   1. 启动后端: cd backend ^&^& python main.py
echo   2. 启动前端: cd frontend ^&^& npm run dev
echo.
pause
