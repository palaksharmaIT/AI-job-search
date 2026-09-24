"""
One-time seed script to populate the Skill table.
Run manually: python -m app.utils.seed_skills

Ports the old hardcoded CANDIDATE_SKILLS list (from skill_matcher.py) into
real Skill rows, plus a few common aliases so matching catches variants
like "Postgres" vs "PostgreSQL".
"""

from app.database.connection import SessionLocal

# Import every model so SQLAlchemy's mapper registry can resolve relationship
# string references (e.g. JobSkill.job -> "Job") before we query anything.
from app.models.job import Job
from app.models.source import Source
from app.models.skill import Skill, JobSkill
from app.models.user import User, UserSkill
from app.models.match_score import MatchScore
from app.models.application import Application

SEED_SKILLS = [
    {"name": "Python", "slug": "python", "aliases": []},
    {"name": "FastAPI", "slug": "fastapi", "aliases": []},
    {"name": "Django", "slug": "django", "aliases": []},
    {"name": "SQL", "slug": "sql", "aliases": []},
    {"name": "PostgreSQL", "slug": "postgresql", "aliases": ["postgres", "psql"]},
    {"name": "REST API", "slug": "rest-api", "aliases": ["restful api", "rest apis"]},
    {"name": "Machine Learning", "slug": "machine-learning", "aliases": ["ml"]},
    {"name": "Artificial Intelligence", "slug": "artificial-intelligence", "aliases": ["ai"]},
    {"name": "LangChain", "slug": "langchain", "aliases": []},
    {"name": "LangGraph", "slug": "langgraph", "aliases": []},
    {"name": "RAG", "slug": "rag", "aliases": ["retrieval augmented generation"]},
]


def seed_skills():
    db = SessionLocal()
    added = 0
    try:
        for entry in SEED_SKILLS:
            existing = db.query(Skill).filter(Skill.slug == entry["slug"]).first()
            if existing:
                continue
            db.add(Skill(**entry))
            added += 1
        db.commit()
        print(f"Seeded {added} new skills ({len(SEED_SKILLS) - added} already existed).")
    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()