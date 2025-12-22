from functools import lru_cache

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from museums.config import settings  # type: ignore  [import-untyped]


@lru_cache
def database_url(db_base: str = settings.DB_BASE) -> str:
    return (
        f"{db_base}://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


# Асинхронный движок для работы с базой данных
engine_async = create_async_engine(url=database_url(settings.DB_BASE_ASYNC))

# Синхронный движок для работы с базой данных
engine = create_engine(url=database_url())

# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)  # type:ignore [call-overload]
session_maker = sessionmaker(bind=engine)
metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    metadata = metadata_obj
    __abstract__ = True
