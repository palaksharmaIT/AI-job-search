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