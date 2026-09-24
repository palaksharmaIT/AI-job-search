from fastapi import APIRouter, HTTPException

from app.services.job_normalizer import (
    import_greenhouse_jobs,
    import_lever_jobs,
    import_ashby_jobs,
    import_career_page_jobs,
)

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/greenhouse/{board_token}")
def ingest_greenhouse(board_token: str):
    try:
        return import_greenhouse_jobs(board_token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Greenhouse ingest failed: {e}")


@router.post("/lever/{site_slug}")
def ingest_lever(site_slug: str, company_name: str):
    try:
        return import_lever_jobs(site_slug, company_name)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lever ingest failed: {e}")


@router.post("/ashby/{org_slug}")
def ingest_ashby(org_slug: str, company_name: str):
    try:
        return import_ashby_jobs(org_slug, company_name)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ashby ingest failed: {e}")


@router.post("/career-page")
def ingest_career_page(url: str, company_name: str):
    try:
        return import_career_page_jobs(url, company_name)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Career page ingest failed: {e}")