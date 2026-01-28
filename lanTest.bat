@echo off
chcp 65001 >nul
echo 切换到局域网测试环境...
echo.

cd /d "%~dp0frontend"
if not exist .env.lan (
    echo 错误: 找不到 .env.lan 文件
    pause
    exit /b 1
)

copy /Y .env.lan .env.local >nul

echo 已切换到局域网测试环境
echo.
echo 配置信息:
echo   - 前端地址: http://0.0.0.0:5173
echo   - 后端地址: http://localhost:8000
echo   - API 路径: /api (通过 Vite 代理)
echo.
echo 下一步操作:
echo   1. 查看本机 IP: ipconfig
echo   2. 启动后端: cd backend ^&^& python main.py
echo   3. 启动前端: cd frontend ^&^& npm run dev
echo   4. 在其他设备访问: http://你的IP:5173
echo.
echo 注意: 确保防火墙允许 5173 和 8000 端口
echo.
pause
