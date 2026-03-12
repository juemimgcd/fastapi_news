from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News
from cache.news_cache import get_cached_categories, set_cache_categories,get_cache_news_list,set_cache_news_list
from fastapi.encoders import jsonable_encoder


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 20):
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    sql = select(Category).offset(skip).limit(limit)
    result = await db.execute(sql)

    categories = result.scalars().all()

    if categories:
        js = jsonable_encoder(categories)
        await set_cache_categories(js)
        return categories
    return []


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    page = skip // limit + 1
    cached_news_list = await get_cache_news_list(category_id, page, limit)
    if cached_news_list:
        return [News(**item) for item in cached_news_list]

    sql = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(sql)

    news_list = result.scalars().all()
    if news_list:
        js = jsonable_encoder(news_list)
        await set_cache_news_list(category_id, page, limit, js)

    return news_list


async def get_news_total(db: AsyncSession, category_id: int):
    sql = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(sql)
    return result.scalar_one()


async def get_news_detail(db: AsyncSession, news_id: int):
    sql = select(News).where(News.id == news_id)
    result = await db.execute(sql)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int):
    sql = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(sql)


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    sql = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(sql)
    return result.scalars().all()
