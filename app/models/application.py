from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.job import Job


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))

    status: Mapped[str] = mapped_column(String(20), default="not_applied")
    # not_applied / drafted / submitted / interviewing / offer / rejected / withdrawn

    # AI-generated outreach (Gemini)
    recruiter_email_draft: Mapped[str | None] = mapped_column(Text, nullable=True)
    recruiter_email_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Playwright autofill
    autofill_attempted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    autofill_succeeded: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    autofill_requires_review: Mapped[bool] = mapped_column(Boolean, default=True)
    autofill_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    job: Mapped["Job"] = relationship(back_populates="applications")