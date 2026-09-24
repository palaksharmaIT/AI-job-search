from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.job import Job
from app.schemas.job import JobCreate

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    existing_job = None

    if job_data.external_job_id:
        existing_job = (
            db.query(Job)
            .filter(
                Job.source == job_data.source,
                Job.external_job_id == job_data.external_job_id
            )
            .first()
        )

    if existing_job:
        return {
            "message": "Job already exists",
            "job": existing_job
        }

    job = Job(
        **job_data.model_dump()
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/")
def get_jobs(
    skill: str | None = None,
    company: str | None = None,
    location: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if skill:
        query = query.filter(
            Job.description.ilike(f"%{skill}%")
        )

    if company:
        query = query.filter(
            Job.company.ilike(f"%{company}%")
        )

    if location:
        query = query.filter(
            Job.location.ilike(f"%{location}%")
        )

    if search:
        query = query.filter(
            Job.title.ilike(f"%{search}%")
        )

    jobs = (
        query
        .order_by(Job.created_at.desc())
        .all()
    )

    return {
        "total": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "source": job.source,
                "external_job_id": job.external_job_id,
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "job_url": job.job_url,
                "apply_url": job.apply_url,
            }
            for job in jobs
        ]
    }