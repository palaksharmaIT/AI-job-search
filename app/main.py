from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.connection import engine

from app.models.job import Job
from app.models.source import Source
from app.models.skill import Skill, JobSkill
from app.models.user import User, UserSkill
from app.models.match_score import MatchScore
from app.models.application import Application

from app.api.routes.jobs import router as jobs_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.applications import router as applications_router
from app.api.routes.emails import router as emails_router
from app.api.routes.dashboard import router as dashboard_router

from app.scheduler.job_scheduler import start_scheduler


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Job Automation System",
    description="AI-powered job discovery and application tracking system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router)
app.include_router(ingest_router)
app.include_router(applications_router)
app.include_router(emails_router)
app.include_router(dashboard_router)

start_scheduler()


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