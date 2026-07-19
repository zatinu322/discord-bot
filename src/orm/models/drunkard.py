from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from .._db import Base


class Drunkard(Base):
    __tablename__ = "drunkard"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        doc="Discord user ID.",
    )

    shots_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False,
        doc="Ananaga shots count",
    )

    drunk_time: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
        doc="Drunk time",
    )

    sobriety_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        doc="Date of unmute",
    )

    removed_role_ids: Mapped[list[int]] = mapped_column(
        ARRAY(BigInteger),
        nullable=False,
        default=list,
        server_default=text('ARRAY[]::bigint[]'),
    )

    def __repr__(self):
        return f"Drunkard #{self.id}"

    def __str__(self):
        return f"Drunkard #{self.id}"
