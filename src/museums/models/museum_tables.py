from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from museums.engines.sqldb import Base  # type: ignore  [import-untyped]


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, category={self.category!r})"


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, location={self.location!r})"


class Museum(Base):
    __tablename__ = "museums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String)  # Название
    address: Mapped[Optional[str]] = mapped_column(String)  # Адрес
    category_id: Mapped[Optional[dict]] = mapped_column(JSONB)  # Категории
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))  # Местоположение
    entity: Mapped[Optional[str]] = mapped_column(String)  # Юридическое лицо
    inn: Mapped[Optional[str]] = mapped_column(String)  # ИНН
    affiliation: Mapped[Optional[str]] = mapped_column(String)  # Принадлежность
    submission: Mapped[Optional[str]] = mapped_column(String)  # Подчинение
    timezone: Mapped[Optional[str]] = mapped_column(String)  # Timezone
    teg: Mapped[Optional[dict]] = mapped_column(JSONB)  # Тэг
    description: Mapped[Optional[str]] = mapped_column(Text)  # Описание
    website: Mapped[Optional[str]] = mapped_column(String)  # Адрес сайта
    email: Mapped[Optional[str]] = mapped_column(String)  # Адрес электронной почты
    eipsk: Mapped[Optional[int]] = mapped_column(Integer)  # Идентификатор ЕИПСК
    service_name: Mapped[Optional[dict]] = mapped_column(JSONB)  # Название сервиса
    updated_at: Mapped[Optional[datetime]]  # Дата обновления

    def __repr__(self) -> str:
        return f"Museum(id={self.id!r}, title={self.title!r})"
