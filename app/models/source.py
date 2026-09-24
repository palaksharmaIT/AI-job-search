from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Source(Base):
    """A configured ingestion source the scheduler polls: a Greenhouse board,
    Lever site, Ashby org, or a scraped career page."""

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(20))  # greenhouse/lever/ashby/career_page
    identifier: Mapped[str] = mapped_column(String(500))  # board token / site slug / org name / URL
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    poll_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    last_polled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)