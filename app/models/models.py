from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class Category(Base):
    __tablename__ = "category"

    category: Mapped["Museums"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, category={self.category!r})"
    

class Location(Base):
    __tablename__ = "location"

    location: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, location={self.location!r})"


class Museums(Base):
    __tablename__ = "museums"

    title: Mapped[str]                                                   # Название
    address: Mapped[Optional[str]]                                       # Адрес
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))  # Местоположение
    entity: Mapped[Optional[str]]                                        # Юридическое лицо
    items: Mapped[list["Category"]] = relationship(                      # Категории
        back_populates="category", cascade="all, delete-orphan"
        )
    inn: Mapped[Optional[int]]                                           # ИНН
    affiliation: Mapped[Optional[str]]                                   # Принадлежность
    submission: Mapped[Optional[str]]                                    # Подчинение
    timezone: Mapped[Optional[str]]                                      # Timezone
    teg = Mapped[JSON]                                                   # Тэг
    description: Mapped[Optional[str]]                                   # Описание
    website: Mapped[Optional[str]]                                       # Адрес сайта
    email: Mapped[Optional[str]]                                         # Адрес электронной почты
    eipsk: Mapped[Optional[int]]                                         # Идентификатор ЕИПСК

    def __repr__(self) -> str:
        return f"Museums(id={self.id!r}, title={self.title!r})"