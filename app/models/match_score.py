from datetime import datetime

from sqlalchemy import Float, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.job import Job
from app.models.job import Job


class MatchScore(Base):
    """Cached match score for a (user, job) pair. Recomputed by the scoring pipeline
    whenever a job is ingested or a user's skills change."""

    __tablename__ = "match_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    score: Mapped[float] = mapped_column(Float)  # 0-100
    scoring_method: Mapped[str] = mapped_column(String(50), default="keyword_overlap_v1")
    computed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    job: Mapped["Job"] = relationship(back_populates="match_scores")