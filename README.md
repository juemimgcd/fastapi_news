# FastAPI News Backend

一个基于 **FastAPI + SQLAlchemy (Async) + MySQL + redis** 构建的新闻管理系统后端项目。项目采用标准的分层架构设计，实现了新闻浏览、分类查询、用户收藏、浏览历史等核心功能。

**项目特点：** 异步高性能、RESTful API 设计、自动数据库迁移（启动时建表）、清晰的分层架构。

---

## 📂 项目结构

```text
fastapi_news/
├── main.py              # 应用入口，注册路由与中间件
├── config/              # 配置文件
│   ├── db_cfg.py        # 数据库连接配置 (SQLAlchemy Async)
│   └── cache_conf.py    # 缓存配置 (Redis)
├── models/              # 数据库 ORM 模型层
│   ├── news.py          # 新闻表模型
│   ├── users.py         # 用户与令牌表模型
│   ├── favorite.py      # 收藏关系表模型
│   └── history.py       # 浏览历史表模型
├── schemas/             # Pydantic 数据验证模型 (请求/响应结构)
├── routers/             # API 路由控制层
│   ├── news.py          # 新闻相关接口 (列表/详情/分类)
│   ├── users.py         # 用户相关接口
│   ├── favorite.py      # 收藏相关接口
│   └── history.py       # 历史记录接口
├── crud/                # 数据库操作逻辑层 (封装 SQL 操作)
├── utils/               # 工具函数与异常处理
└── test_main.http       # API 测试脚本
```

---

## 🛠️ 技术栈

- **框架**: FastAPI（高性能异步 Web 框架）
- **ORM**: SQLAlchemy（2.0+ Async 模式）
- **数据库**: MySQL / MariaDB
- **数据验证**: Pydantic
- **语言**: Python 3.8+

---

## ⚡ 快速开始

### 1) 环境准备

确保已安装：
- Python 3.8+
- MySQL（或 MariaDB）

### 2) 安装依赖

如果项目有 `requirements.txt`，推荐使用：

```bash
pip install -r requirements.txt
```

若无，可先按如下安装（按需补充）：

```bash
pip install fastapi sqlalchemy pymysql uvicorn pydantic
```

> 说明：若你使用的是 SQLAlchemy Async + MySQL，常见还会用到 `aiomysql` 或 `asyncmy`（取决于你的数据库驱动选择）。

### 3) 配置数据库

修改 `config/db_cfg.py` 中的数据库连接字符串，例如：

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/fastapi_news"
```

### 4) 启动服务

使用 Uvicorn 启动开发服务器：

```bash
uvicorn main:app --reload
```

启动后可访问自动生成的 API 文档：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 📡 API 接口说明

项目主要包含以下四大模块的 API 接口：

### 新闻模块 (`/api/news`)

- `GET /categories`：获取新闻分类列表  
- `GET /list`：分页获取指定分类下的新闻列表  
  - 参数：`categoryId`, `page`, `pageSize`
- `GET /detail`：获取新闻详情（自动增加浏览量）  
  - 参数：`id`  
  - 返回：包含相关新闻推荐

### 用户模块 (`/api/users`)

- 用户注册、登录、信息管理  
- 基于 Token 的身份验证机制（`UserToken` 表）

### 收藏模块 (`/api/favorite`)

- 用户收藏新闻、取消收藏、查看收藏列表  
- 唯一约束：同一用户对同一新闻只能收藏一次

### 历史模块 (`/api/history`)

- 自动/手动记录用户浏览历史  
- 按时间排序查看历史记录

---

## 🏗️ 核心设计

### 数据库模型（Models）

项目使用 SQLAlchemy 的 `DeclarativeBase` 定义 ORM 模型，主要包含：

- **User**：存储用户基本信息（用户名、加密密码、头像、性别等）
- **News**：存储新闻内容、分类、浏览量等
- **Favorite**：关联用户与新闻的收藏关系表
- **History**：记录用户浏览新闻的时间戳

### 异步数据库会话

在 `main.py` 中通过 `lifespan` 事件管理器，在应用启动时自动创建数据库表结构：

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
```

### 跨域支持

默认开启了 CORS 中间件，允许所有来源的请求（开发环境）。生产环境建议限制具体域名。

---

## 🤝 贡献

欢迎提交 Issue 或 Pull Request 来改进这个项目！

---

## 📄 许可证

MIT License

---

