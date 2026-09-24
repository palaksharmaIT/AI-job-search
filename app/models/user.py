from sqlalchemy import String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_text: Mapped[str | None] = mapped_column(String, nullable=True)  # used for Gemini email context
    min_match_score: Mapped[float] = mapped_column(Float, default=0.0)
    preferred_locations: Mapped[list] = mapped_column(JSON, default=list)
    remote_only: Mapped[bool] = mapped_column(Boolean, default=False)


class UserSkill(Base):
    """A skill the user has, with a weight used in match scoring."""

    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    weight: Mapped[float] = mapped_column(Float, default=1.0)  # proficiency/importance

    skill: Mapped["Skill"] = relationship()