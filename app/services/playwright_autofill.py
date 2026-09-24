"""
Fills known fields on a supported application form using the user's profile,
then STOPS before final submission - a human must review and click submit
themselves. This never auto-submits, by design (Application.autofill_requires_review
defaults to True and stays True unless a human explicitly overrides it).

There's no universal application-form schema, so like career_pages.py, this
needs a per-site field-selector config.
"""

from datetime import datetime

from playwright.sync_api import sync_playwright

from app.database.connection import SessionLocal
from app.models.user import User
from app.models.application import Application

# Per-ATS/site selector config, keyed by hostname of the apply_url.
FORM_CONFIGS = {
    # "boards.greenhouse.io": {
    #     "full_name": "input[name='job_application[name]']",
    #     "email": "input[name='job_application[email]']",
    #     "resume_upload": "input[type='file'][name='resume']",
    # },
}


def autofill_application(user_id: int, job_id: int, apply_url: str, resume_path: str | None = None):
    from urllib.parse import urlparse

    hostname = urlparse(apply_url).netloc
    config = FORM_CONFIGS.get(hostname)

    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        application = (
            db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )
        if not application:
            application = Application(user_id=user_id, job_id=job_id)
            db.add(application)

        if not config:
            application.autofill_attempted_at = datetime.utcnow()
            application.autofill_succeeded = False
            application.autofill_notes = f"No form config for {hostname} - add one to FORM_CONFIGS."
            db.commit()
            return {"success": False, "reason": "no_config", "hostname": hostname}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # visible so human can review before submitting
            page = browser.new_page()
            page.goto(apply_url, timeout=30000)

            if config.get("full_name") and user.full_name:
                page.fill(config["full_name"], user.full_name)
            if config.get("email"):
                page.fill(config["email"], user.email)
            if config.get("resume_upload") and resume_path:
                page.set_input_files(config["resume_upload"], resume_path)

            # Deliberately NOT calling any submit button here.
            # Browser stays open for the human to review and submit manually.

        application.autofill_attempted_at = datetime.utcnow()
        application.autofill_succeeded = True
        application.autofill_requires_review = True
        application.autofill_notes = "Fields filled. Awaiting human review and manual submit."
        db.commit()

        return {"success": True, "requires_review": True}

    except Exception as e:
        application.autofill_attempted_at = datetime.utcnow()
        application.autofill_succeeded = False
        application.autofill_notes = f"Autofill error: {e}"
        db.commit()
        return {"success": False, "reason": str(e)}

    finally:
        db.close()