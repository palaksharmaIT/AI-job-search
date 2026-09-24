from app.collectors.greenhouse import get_greenhouse_jobs
from app.collectors.lever import get_lever_jobs
from app.collectors.ashby import get_ashby_jobs
from app.models.job import Job
from app.database.connection import SessionLocal
from app.collectors.career_pages import get_career_page_jobs


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

            title = job.get("title") or ""
            company = job.get("company_name") or ""
            location = job.get("location", {}).get("name") or ""

            new_job = Job(
                source="greenhouse",
                external_job_id=str(job["id"]),
                company=company,
                title=title,
                description=job.get("content"),
                location=location,
                job_url=job.get("absolute_url"),
                apply_url=job.get("absolute_url"),
                dedup_hash=Job.compute_dedup_hash(title, company, location),
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


def import_lever_jobs(site_slug: str, company_name: str):
    """Lever postings don't include a company name field the way Greenhouse
    does, so it's passed in explicitly (usually the same as site_slug,
    capitalized, or whatever display name you want stored)."""

    jobs = get_lever_jobs(site_slug)

    db = SessionLocal()

    added = 0
    skipped = 0

    try:
        for job in jobs:
            existing_job = (
                db.query(Job)
                .filter(
                    Job.source == "lever",
                    Job.external_job_id == job["id"]
                )
                .first()
            )

            if existing_job:
                skipped += 1
                continue

            title = job.get("text") or ""
            location = (job.get("categories") or {}).get("location") or ""
            description = job.get("descriptionPlain") or job.get("description") or ""

            new_job = Job(
                source="lever",
                external_job_id=job["id"],
                company=company_name,
                title=title,
                description=description,
                location=location,
                job_url=job.get("hostedUrl"),
                apply_url=job.get("applyUrl"),
                dedup_hash=Job.compute_dedup_hash(title, company_name, location),
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


def import_ashby_jobs(org_slug: str, company_name: str):
    jobs = get_ashby_jobs(org_slug)

    db = SessionLocal()

    added = 0
    skipped = 0

    try:
        for job in jobs:
            existing_job = (
                db.query(Job)
                .filter(
                    Job.source == "ashby",
                    Job.external_job_id == job["id"]
                )
                .first()
            )

            if existing_job:
                skipped += 1
                continue

            title = job.get("title") or ""
            location = job.get("location") or ""

            new_job = Job(
                source="ashby",
                external_job_id=job["id"],
                company=company_name,
                title=title,
                description=job.get("descriptionHtml"),
                location=location,
                remote=bool(job.get("isRemote")),
                job_url=job.get("jobUrl"),
                apply_url=job.get("applyUrl"),
                dedup_hash=Job.compute_dedup_hash(title, company_name, location),
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


def import_career_page_jobs(url: str, company_name: str):
    jobs = get_career_page_jobs(url)

    db = SessionLocal()

    added = 0
    skipped = 0

    try:
        for job in jobs:
            title = job.get("title") or ""
            location = job.get("location") or ""

            # No stable external ID on most career pages, so dedup relies
            # entirely on the content hash (title + company + location).
            dedup_hash = Job.compute_dedup_hash(title, company_name, location)

            existing_job = (
                db.query(Job)
                .filter(Job.dedup_hash == dedup_hash)
                .first()
            )

            if existing_job:
                skipped += 1
                continue

            new_job = Job(
                source="career_page",
                external_job_id=None,
                company=company_name,
                title=title,
                description=None,
                location=location,
                job_url=job.get("job_url"),
                apply_url=job.get("job_url"),
                dedup_hash=dedup_hash,
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