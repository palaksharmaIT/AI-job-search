from fastapi import APIRouter, HTTPException

from app.services.email_generator import generate_recruiter_email

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/generate")
def generate_email(user_id: int, job_id: int):
    try:
        return generate_recruiter_email(user_id, job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Email generation failed: {e}")