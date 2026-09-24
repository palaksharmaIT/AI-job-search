"""
One-time script: drops ALL tables and recreates them fresh from the current
models. Use this when a model's columns changed but create_all() didn't pick
it up (create_all only creates missing tables, never alters existing ones).

WARNING: this deletes all existing data. Fine for dev/testing; do NOT run
this against a database with real data you want to keep.

Run: python -m app.utils.reset_db
"""

from app.database.base import Base
from app.database.connection import engine

# Import every model so Base.metadata knows about all tables.
from app.models.job import Job
from app.models.source import Source
from app.models.skill import Skill, JobSkill
from app.models.user import User, UserSkill
from app.models.match_score import MatchScore
from app.models.application import Application


def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating all tables from current models...")
    Base.metadata.create_all(bind=engine)
    print("Done. Run seed_skills.py again if you need the Skill table populated.")


if __name__ == "__main__":
    confirm = input("This will DELETE all data in the database. Type 'yes' to continue: ")
    if confirm.strip().lower() == "yes":
        reset_db()
    else:
        print("Cancelled.")