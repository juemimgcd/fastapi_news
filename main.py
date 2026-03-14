from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.db_cfg import engine,Base
from routers import favorite, history, news, users
from utils.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)  # 开发环境
    yield

    await engine.dispose()


app = FastAPI(
    title="news_app",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)


@app.get("/")
async def root():
    return {"code": 200, "message": "ok", "data": None}
