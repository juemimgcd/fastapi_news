from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
url = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

engine = create_async_engine(
    url,
    echo=False,
    pool_size=10,
    max_overflow=20
)

session_local = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False

)


class Base(DeclarativeBase):
    pass


async def get_database():
    async with session_local() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
