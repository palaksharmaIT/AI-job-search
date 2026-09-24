from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

# Import every model so Base.metadata knows about all tables before create_all().
from app.models.job import Job
from app.models.source import Source
from app.models.skill import Skill, JobSkill
from app.models.user import User, UserSkill
from app.models.match_score import MatchScore
from app.models.application import Application

from app.api.routes.jobs import router as jobs_router
from app.api.routes.ingest import router as ingest_router
from app.scheduler.job_scheduler import start_scheduler


Base.metadata.create_all(bind=engine)

scheduler = start_scheduler()

app = FastAPI(
    title="Job Automation System",
    description="AI-powered job discovery and application tracking system",
    version="1.0.0"
)


app.include_router(jobs_router)
app.include_router(ingest_router)


@app.get("/")
def home():
    return {
        "message": "Job Automation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }