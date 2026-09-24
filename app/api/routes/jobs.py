from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.connection import get_db
from app.models.job import Job
from app.models.match_score import MatchScore
from app.schemas.job import JobCreate, JobRead, JobReadWithScore

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobRead)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    existing_job = None

    # Prefer exact source-level dedup when we have an external ID.
    if job_data.external_job_id:
        existing_job = (
            db.query(Job)
            .filter(
                Job.source == job_data.source,
                Job.external_job_id == job_data.external_job_id,
            )
            .first()
        )

    dedup_hash = Job.compute_dedup_hash(job_data.title, job_data.company, job_data.location or "")

    # Fall back to content-based dedup so the same role cross-posted to a
    # different board (or reposted with a new external ID) doesn't duplicate.
    if not existing_job:
        existing_job = db.query(Job).filter(Job.dedup_hash == dedup_hash).first()

    if existing_job:
        existing_job.last_seen_at = existing_job.last_seen_at  # bump via onupdate on commit
        db.commit()
        db.refresh(existing_job)
        return existing_job

    job = Job(**job_data.model_dump(), dedup_hash=dedup_hash)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/", response_model=list[JobReadWithScore])
def list_jobs(
    db: Session = Depends(get_db),
    user_id: int | None = Query(None, description="Include match_score for this user"),
    company: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
    min_score: float | None = Query(None, description="Requires user_id"),
    status: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    query = db.query(Job)

    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if remote is not None:
        query = query.filter(Job.remote == remote)
    if status:
        query = query.filter(Job.status == status)

    jobs = query.order_by(Job.posted_at.desc().nullslast()).offset(offset).limit(limit).all()

    results = []
    for job in jobs:
        score = None
        if user_id:
            match = (
                db.query(MatchScore)
                .filter(MatchScore.user_id == user_id, MatchScore.job_id == job.id)
                .first()
            )
            score = match.score if match else None
            if min_score is not None and (score is None or score < min_score):
                continue
        item = JobReadWithScore.model_validate(job)
        item.match_score = score
        results.append(item)

    if user_id:
        results.sort(key=lambda j: (j.match_score is None, -(j.match_score or 0)))

    return results


@router.get("/{job_id}", response_model=JobReadWithScore)
def get_job(job_id: int, user_id: int | None = None, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    item = JobReadWithScore.model_validate(job)
    if user_id:
        match = (
            db.query(MatchScore)
            .filter(MatchScore.user_id == user_id, MatchScore.job_id == job_id)
            .first()
        )
        item.match_score = match.score if match else None
    return item