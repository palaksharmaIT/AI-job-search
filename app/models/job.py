from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    external_job_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )

    company: Mapped[str] = mapped_column(
        String(255)
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    job_url: Mapped[str] = mapped_column(
        Text
    )

    apply_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )