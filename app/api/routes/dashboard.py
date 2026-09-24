from fastapi import APIRouter

from app.database.connection import SessionLocal
from app.models.job import Job
from app.models.application import Application
from app.models.match_score import MatchScore

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(user_id: int):
    db = SessionLocal()
    try:
        total_jobs = db.query(Job).count()
        matched_jobs = db.query(MatchScore).filter(MatchScore.user_id == user_id).count()

        applications = db.query(Application).filter(Application.user_id == user_id).all()
        by_status = {}
        for app_row in applications:
            by_status[app_row.status] = by_status.get(app_row.status, 0) + 1

        top_matches = (
            db.query(MatchScore)
            .filter(MatchScore.user_id == user_id)
            .order_by(MatchScore.score.desc())
            .limit(5)
            .all()
        )

        return {
            "total_jobs": total_jobs,
            "matched_jobs": matched_jobs,
            "applications_by_status": by_status,
            "top_match_job_ids": [m.job_id for m in top_matches],
        }
    finally:
        db.close()