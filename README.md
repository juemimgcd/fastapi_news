# FastAPI News Backend

一个基于 **FastAPI + SQLAlchemy Async + MySQL + Redis** 的新闻系统后端示例项目，提供新闻列表/详情/分类、用户体系、收藏、浏览历史等常用能力，并包含 Alembic 迁移配置，适合作为中小型 API 项目的参考模板。

---

## Features

- **异步 API**：FastAPI + SQLAlchemy Async
- **分层结构清晰**：routers / schemas / crud / models / utils
- **新闻模块**：分类、分页列表、详情、浏览量、相关推荐
- **用户模块**：注册/登录、Token 认证（基于数据表存储）
- **收藏模块**：收藏/取消收藏/收藏列表（同一用户同一新闻唯一约束）
- **历史模块**：记录用户浏览历史，支持按时间查询
- **数据库迁移**：已包含 `alembic.ini` 与 `alembic/` 目录（可扩展标准迁移流程）

---

## Tech Stack

- **Python**: 3.8+
- **Web**: FastAPI, Uvicorn
- **ORM**: SQLAlchemy 2.x (Async)
- **DB**: MySQL / MariaDB
- **Cache**: Redis（项目中有 `cache/` 与相关配置）
- **Migration**: Alembic
- **Validation**: Pydantic

---

## Project Structure

```text
fastapi_news/
├── main.py               # 应用入口：注册路由、中间件、生命周期事件等
├── config/               # 配置（数据库、缓存等）
├── models/               # ORM Models
├── schemas/              # Pydantic Schemas（请求/响应）
├── crud/                 # 数据访问层（封装 SQL 操作）
├── routers/              # 路由层（业务接口）
├── utils/                # 工具函数、异常处理等
├── cache/                # 缓存相关封装（如有）
├── alembic/              # Alembic 迁移脚本目录
├── alembic.ini           # Alembic 配置
├── requirements.txt      # 依赖
├── .env_example          # 环境变量示例（建议复制为 .env）
└── test_main.http        # 简单接口测试脚本（IDE 可直接运行）
```

---

## Quick Start

### 1. 创建并激活虚拟环境（推荐）
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
仓库提供了 `.env_example`，建议：
```bash
cp .env_example .env
```

然后按你的本地环境修改数据库 / Redis 配置（具体读取方式以代码为准；如果你希望 README 写得更“精准到字段”，我也可以再把配置文件内容读出来对齐）。

### 4. 启动服务
```bash
uvicorn main:app --reload
```

访问接口文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Overview（路由以实际代码为准）

### News
- `GET /api/news/categories`：获取分类列表
- `GET /api/news/list`：分页获取分类下新闻
  - query: `categoryId`, `page`, `pageSize`
- `GET /api/news/detail`：新闻详情（可能会自增浏览量）
  - query: `id`
  - response: 可能包含相关推荐

### Users
- 注册 / 登录 / 用户信息
- Token 鉴权（项目使用 `UserToken` 表思路）

### Favorite
- 收藏/取消收藏/收藏列表
- 同一用户同一新闻仅允许一条收藏记录（唯一约束）

### History
- 记录浏览历史
- 按时间排序查询

---

## Database & Migration

项目包含 Alembic 配置（`alembic.ini`、`alembic/`）。常见使用方式：

- 生成迁移（示例）：
```bash
alembic revision --autogenerate -m "init"
```

- 执行迁移：
```bash
alembic upgrade head
```

> 说明：如果你当前在 `main.py` 里使用 lifespan 启动时自动 `create_all`，建议在生产环境逐步迁移到 **Alembic 管理 schema**，避免自动建表造成不可控变更。

---

## Development Notes

### 建议忽略的文件
建议将以下内容加入 `.gitignore`：
- `.idea/`（JetBrains IDE 配置）
- `.venv/`
- `__pycache__/`
- `.env`（敏感信息）

---

## License
MIT



MIT License

---

