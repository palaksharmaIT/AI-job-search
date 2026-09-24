from fastapi import APIRouter, HTTPException

from app.schemas.application import ApplicationCreate, ApplicationStatusUpdate, ApplicationRead
from app.services.application_service import (
    get_or_create_application,
    update_application_status,
    list_applications_for_user,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationRead)
def create_application(data: ApplicationCreate):
    return get_or_create_application(data.user_id, data.job_id)


@router.patch("/status", response_model=ApplicationRead)
def update_status(user_id: int, job_id: int, data: ApplicationStatusUpdate):
    try:
        return update_application_status(user_id, job_id, data.status, data.notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[ApplicationRead])
def get_user_applications(user_id: int):
    return list_applications_for_user(user_id)