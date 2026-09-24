from app.collectors.greenhouse import get_greenhouse_jobs
from app.models.job import Job
from app.database.connection import SessionLocal


def import_greenhouse_jobs(board_token: str):
    jobs = get_greenhouse_jobs(board_token)

    db = SessionLocal()

    added = 0
    skipped = 0

    try:
        for job in jobs:
            existing_job = (
                db.query(Job)
                .filter(
                    Job.source == "greenhouse",
                    Job.external_job_id == str(job["id"])
                )
                .first()
            )

            if existing_job:
                skipped += 1
                continue

            new_job = Job(
                source="greenhouse",
                external_job_id=str(job["id"]),
                company=job.get("company_name"),
                title=job.get("title"),
                description=job.get("content"),
                location=job.get("location", {}).get("name"),
                job_url=job.get("absolute_url"),
                apply_url=job.get("absolute_url"),
            )

            db.add(new_job)
            added += 1

        db.commit()

        return {
            "total_fetched": len(jobs),
            "added": added,
            "skipped": skipped,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()