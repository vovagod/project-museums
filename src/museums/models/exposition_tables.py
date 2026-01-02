from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text, Enum, DateTime, func
#from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM

from museums.engines.sqldb import Base  # type: ignore  [import-untyped]
from museums.models.museum_tables import Museum  # development

#class Visitors(enum.Enum):
    #ADULT = "adult"
    #CHILD = "child"
    #ALL = "all"

#metadata = Base.metadata

Visitors = ENUM(
    "adult", "child", "all",
    name="enum_visitor",  # Database type name (critical!)
    #metadata=metadata_obj  # Attach to the base metadata (optional but safe)
)

class Exposition(Base):
    __tablename__ = "expositions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    museum_id: Mapped[int] = mapped_column(ForeignKey("museums.id", ondelete="CASCADE"))
    _museum: Mapped["Museum"] = relationship(back_populates="_exposition")
    entity: Mapped[str] = mapped_column(String)
    branch: Mapped[str] = mapped_column(String)
    showcase: Mapped[str] = mapped_column(String)
    history: Mapped[str] = mapped_column(Text)
    webpage: Mapped[str] = mapped_column(String(255))
    visitors: Mapped[Enum] = mapped_column(Visitors, default="all")
    period: Mapped[Optional[str]] = mapped_column(String)
    price: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"Exposition(id={self.id!r}, name={self.name!r})"