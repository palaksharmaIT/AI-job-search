from sqlalchemy import String, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)  # normalized, e.g. "postgresql"
    aliases: Mapped[list] = mapped_column(JSON, default=list)  # e.g. ["postgres", "psql"]


class JobSkill(Base):
    """Through table: which skills appear on a job, with extraction confidence."""

    __tablename__ = "job_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    confidence: Mapped[float] = mapped_column(Float, default=1.0)

    job: Mapped["Job"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship()