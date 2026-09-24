"""
Generates a personalized recruiter outreach email via Gemini. Always saved
as a draft on Application.recruiter_email_draft for human review - never
auto-sends.

Setup:
  pip install google-generativeai
Add to app/core/config.py's Settings class:
  gemini_api_key: str
Add to .env:
  GEMINI_API_KEY=your_key_here
"""

import google.generativeai as genai

from app.core.config import settings
from app.database.connection import SessionLocal
from app.models.job import Job
from app.models.user import User
from app.models.application import Application

genai.configure(api_key=settings.gemini_api_key)

PROMPT_TEMPLATE = """\
Write a concise, personalized outreach email to a recruiter about this job.
Keep it under 150 words, professional but warm, no generic filler.

Candidate background:
{resume_text}

Job:
Title: {title}
Company: {company}
Description excerpt: {description}

Output only the email body, no subject line, no placeholders like [Name].
"""


def generate_recruiter_email(user_id: int, job_id: int):
    db = SessionLocal()

    try:
        user = db.get(User, user_id)
        job = db.get(Job, job_id)

        if not user or not job:
            raise ValueError("User or Job not found")

        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = PROMPT_TEMPLATE.format(
            resume_text=(user.resume_text or "Experienced software engineer.")[:2000],
            title=job.title,
            company=job.company,
            description=(job.description or "")[:1500],
        )

        response = model.generate_content(prompt)
        draft_text = response.text.strip()

        application = (
            db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )

        if not application:
            application = Application(user_id=user_id, job_id=job_id)
            db.add(application)

        application.recruiter_email_draft = draft_text
        if application.status == "not_applied":
            application.status = "drafted"

        db.commit()
        db.refresh(application)

        return {
            "application_id": application.id,
            "status": application.status,
            "email_draft": application.recruiter_email_draft,
        }

    finally:
        db.close()