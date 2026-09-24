from datetime import datetime

from app.database.connection import SessionLocal
from app.models.application import Application

VALID_STATUSES = {
    "not_applied", "drafted", "submitted",
    "interviewing", "offer", "rejected", "withdrawn",
}


def get_or_create_application(user_id: int, job_id: int) -> Application:
    db = SessionLocal()
    try:
        app_row = (
            db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )
        if app_row:
            return app_row

        app_row = Application(user_id=user_id, job_id=job_id)
        db.add(app_row)
        db.commit()
        db.refresh(app_row)
        return app_row
    finally:
        db.close()


def update_application_status(user_id: int, job_id: int, status: str, notes: str | None = None) -> Application:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {VALID_STATUSES}")

    db = SessionLocal()
    try:
        app_row = (
            db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )
        if not app_row:
            app_row = Application(user_id=user_id, job_id=job_id)
            db.add(app_row)

        app_row.status = status
        if notes is not None:
            app_row.notes = notes
        if status == "submitted" and not app_row.applied_at:
            app_row.applied_at = datetime.utcnow()

        db.commit()
        db.refresh(app_row)
        return app_row
    finally:
        db.close()


def list_applications_for_user(user_id: int) -> list[Application]:
    db = SessionLocal()
    try:
        return db.query(Application).filter(Application.user_id == user_id).all()
    finally:
        db.close()