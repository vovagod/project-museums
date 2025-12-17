from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, MetaData
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.engines.sqldb import Base


class Category(Base):
    __tablename__ = "categories"

    #id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, category={self.category!r})"
    

class Location(Base):
    __tablename__ = "locations"

    #id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    #location: Mapped[List["Museum"]] = relationship(
        ##"Museum",
        #back_populates="locations",
        #cascade="all, delete",
        #passive_deletes=True,
    #)
    #location: Mapped[List["Museum"]] = relationship()
    #museums: Mapped[List["Museum"]] = relationship('Museum', back_populates='location')

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, location={self.location!r})"


class Museum(Base):
    __tablename__ = "museums"

    #id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String)                                                   # Название
    address: Mapped[Optional[str]] = mapped_column(String)                                      # Адрес
    category_id: Mapped[Optional[dict]] = mapped_column(JSONB)               # Категории
    location_id: Mapped[int] = mapped_column(  
        #Integer,                          # Местоположение
        ForeignKey("locations.id",
        ondelete="CASCADE")
    )  
    #museum: Mapped["Location"] = relationship(
        ##"Location",
        #back_populates="location"
        #)     
    #location = relationship('Location', back_populates='museums')   

    entity: Mapped[Optional[str]] = mapped_column(String)                                       # Юридическое лицо
    inn: Mapped[Optional[str]] = mapped_column(String)                                         # ИНН
    affiliation: Mapped[Optional[str]] = mapped_column(String)                                  # Принадлежность
    submission: Mapped[Optional[str]] = mapped_column(String)                                   # Подчинение
    timezone: Mapped[Optional[str]] = mapped_column(String)                                     # Timezone
    teg: Mapped[Optional[dict]] = mapped_column(JSONB)                                                   # Тэг
    description: Mapped[Optional[str]] = mapped_column(Text)                                   # Описание
    website: Mapped[Optional[str]] = mapped_column(String)                                       # Адрес сайта
    email: Mapped[Optional[str]] = mapped_column(String)                                         # Адрес электронной почты
    eipsk: Mapped[Optional[int]]= mapped_column(Integer)                                         # Идентификатор ЕИПСК
    service_name: Mapped[Optional[dict]] = mapped_column(JSONB)           # Название сервиса
    updated_at: Mapped[Optional[datetime]]                               # Дата обновления


    def __repr__(self) -> str:
        return f"Museum(id={self.id!r}, title={self.title!r})"