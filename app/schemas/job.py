from pydantic import BaseModel


class JobCreate(BaseModel):
    source: str
    external_job_id: str | None = None
    company: str
    title: str
    description: str | None = None
    location: str | None = None
    job_url: str
    apply_url: str | None = None