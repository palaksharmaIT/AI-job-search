from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine
from app.models.job import Job
from app.api.routes.jobs import router as jobs_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Job Automation System",
    description="AI-powered job discovery and application tracking system",
    version="1.0.0"
)


app.include_router(jobs_router)


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