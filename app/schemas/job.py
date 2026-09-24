from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    source: str
    external_job_id: str | None = None
    company: str
    title: str
    description: str | None = None
    location: str | None = None
    remote: bool | None = None
    job_url: str
    apply_url: str | None = None
    posted_at: datetime | None = None


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    company: str
    title: str
    description: str | None = None
    location: str | None = None
    remote: bool | None = None
    job_url: str
    apply_url: str | None = None
    status: str
    posted_at: datetime | None = None
    created_at: datetime


class JobReadWithScore(JobRead):
    match_score: float | None = None