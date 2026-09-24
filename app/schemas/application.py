from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int


class ApplicationStatusUpdate(BaseModel):
    status: str  # not_applied/drafted/submitted/interviewing/offer/rejected/withdrawn
    notes: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    job_id: int
    status: str
    recruiter_email_draft: str | None = None
    autofill_succeeded: bool | None = None
    autofill_requires_review: bool
    notes: str | None = None
    applied_at: datetime | None = None
    created_at: datetime
    updated_at: datetime