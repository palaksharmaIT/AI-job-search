import hashlib
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(100))  # kept for backward compat / quick filtering
    external_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    job_url: Mapped[str] = mapped_column(Text)
    apply_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Dedup key: hash of normalized (title, company, location). Catches the same
    # role cross-posted to multiple boards or reposted after a minor edit.
    dedup_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    status: Mapped[str] = mapped_column(String(20), default="new")  # new/reviewed/archived/expired

    posted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    skills: Mapped[list["JobSkill"]] = relationship(back_populates="job")
    match_scores: Mapped[list["MatchScore"]] = relationship(back_populates="job")
    applications: Mapped[list["Application"]] = relationship(back_populates="job")

    @staticmethod
    def compute_dedup_hash(title: str, company: str, location: str) -> str:
        normalized = f"{title.strip().lower()}|{company.strip().lower()}|{(location or '').strip().lower()}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()