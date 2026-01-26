# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 项目概述

MediTrack 是一个面向患者的药物管理平台，后端使用 FastAPI，前端使用 Vue 3。

## 架构

### 后端 (FastAPI + SQLAlchemy)

**位置**: `backend/`

**核心结构**:
- `main.py` - 应用程序入口点，FastAPI 应用初始化，CORS 中间件配置，路由注册
- `src/core/config.py` - 使用 pydantic-settings 进行配置管理，从 `.env` 文件读取配置
- `src/db/database.py` - SQLAlchemy 设置，包含引擎、Base、会话工厂和 `get_db()` 依赖
- `src/db/models/` - SQLAlchemy ORM 模型
  - `user.py` - 用户模型（包含用户名、邮箱、明文密码、头像Base64、账户状态等）
- `src/api/` - API 路由处理器（控制器层）
  - `user.py` - 用户相关API（注册、登录、获取/更新用户信息、上传头像）
- `src/schemas/` - Pydantic 模式，用于请求/响应验证
  - `user.py` - 用户相关的请求/响应模式
- `src/serves/` - 业务逻辑/服务层
  - `user_service.py` - 用户业务逻辑（JWT生成、用户CRUD）

**数据库**: SQLite 配合 SQLAlchemy ORM。数据库文件位置通过 `.env` 中的 `DATA_URL` 配置。

**配置**: 使用 pydantic-settings 从 `backend/.env` 加载：
- `HOST` - 服务器主机（默认：127.0.0.1）
- `PORT` - 服务器端口（默认：8000）
- `DATA_URL` - 数据库连接字符串
- `SECRET_KEY` - JWT密钥（生产环境必须修改）

**已安装的关键依赖**:
- `fastapi` - Web框架
- `sqlalchemy` - ORM
- `uvicorn` - ASGI服务器
- `pydantic-settings` - 配置管理
- `python-jose[cryptography]` - JWT处理
- `python-multipart` - 文件上传支持
- `email-validator` - 邮箱验证

### 前端 (Vue 3 + Vite)

**位置**: `frontend/`

**结构**:
- `src/main.js` - Vue 应用入口点
- `src/App.vue` - 根组件
- `vite.config.js` - Vite 配置，`@` 别名指向 `src/`

**构建工具**: Vite 配合 Vue 3 插件和 Vue DevTools

## 开发命令

### 后端

**前置要求**: Python >=3.10，使用 `uv` 进行依赖管理

```bash
cd backend

# 安装依赖（使用 uv）
uv sync

# 运行开发服务器
python main.py
# 服务器运行在 http://127.0.0.1:8000（可通过 .env 配置）

# 访问 API 文档
# http://127.0.0.1:8000/docs (Swagger UI)
# http://127.0.0.1:8000/redoc (ReDoc)
```

### 前端

**前置要求**: Node.js ^20.19.0 || >=22.12.0

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 生产环境构建
npm run build

# 预览生产构建
npm run preview
```

## 关键模式

### 后端模式

1. **三级分层架构**: 严格遵循 API路由层 → 业务逻辑层 → ORM数据库层
   - `api/` - 路由处理器（控制器），处理HTTP请求/响应，调用服务层
   - `serves/` - 业务逻辑（服务），包含核心业务逻辑，不直接处理HTTP
   - `db/models/` - 数据库模型，定义数据结构
   - `schemas/` - Pydantic模型，用于数据验证和序列化

2. **配置管理**: 所有环境特定的设置都放在 `backend/.env` 中，通过 `src/core/config.py` 加载

3. **数据库会话**: 使用 `get_db()` 依赖注入模式：
   ```python
   from src.db.database import get_db
   from fastapi import Depends
   from sqlalchemy.orm import Session

   @router.get("/endpoint")
   def endpoint(db: Session = Depends(get_db)):
       # 在这里使用 db 会话
   ```

4. **用户认证**:
   - 使用 JWT Bearer Token 认证
   - 密码使用明文存储（注意：仅用于开发/学习环境）
   - 通过 `get_current_user` 依赖获取当前登录用户
   ```python
   from src.api.user import get_current_user

   @router.get("/protected")
   async def protected_route(current_user: UserResponse = Depends(get_current_user)):
       # current_user 包含当前登录用户信息
   ```

5. **头像处理**:
   - 使用 Base64 编码直接存储在数据库中
   - 格式：`data:image/jpeg;base64,...`
   - 支持 JPEG、PNG、GIF、WEBP
   - 限制大小为 5MB

6. **模型定义**: SQLAlchemy 模型继承自 `src.db.database` 导入的 `Base`

7. **路由注册**: 在 `main.py` 中使用 `app.include_router()` 注册路由

8. **生命周期管理**: 使用 `lifespan` 上下文管理器进行应用启动/关闭时的初始化

### 前端模式

1. **路径别名**: 使用 `@/` 引用 `src/` 目录（在 vite.config.js 中配置）

2. **Vue 3 组合式 API**: 项目使用 `<script setup>` 语法

## 已实现的功能

### 用户管理模块
- **POST /user/register** - 用户注册（返回用户信息和JWT token）
- **POST /user/login** - 用户登录（支持用户名或邮箱登录）
- **GET /user/me** - 获取当前用户信息（需要认证）
- **PUT /user/me** - 更新当前用户信息（需要认证）
- **POST /user/avatar** - 上传用户头像Base64（需要认证）

## 开发指南

### 添加新的API端点

1. 在 `src/db/models/` 中定义ORM模型（如需要）
2. 在 `src/schemas/` 中定义请求/响应的Pydantic模型
3. 在 `src/serves/` 中实现业务逻辑
4. 在 `src/api/` 中创建路由处理器
5. 在 `main.py` 中注册路由

### 数据库迁移

当修改ORM模型后：
1. 删除现有数据库文件（开发环境）
2. 重启应用，`init_db()` 会自动创建新表结构

生产环境建议使用 Alembic 进行数据库迁移。

## 注意事项

- 后端代码使用中文注释
- CORS 配置为允许所有来源（`allow_origins=["*"]`）- 生产环境应限制
- PyPI 镜像配置为使用清华大学镜像（在 `pyproject.toml` 中）
- 数据库初始化在应用启动时自动执行（通过 `lifespan` 管理）
- JWT密钥 `SECRET_KEY` 在生产环境必须修改为强随机字符串
- 头像使用 Base64 编码存储，前端可直接在 `<img>` 标签的 `src` 属性中使用
- **密码采用明文存储，仅适用于开发/学习环境，生产环境必须使用加密存储**
