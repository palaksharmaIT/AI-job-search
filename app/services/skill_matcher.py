"""
v1 matching pipeline: keyword/alias overlap between a job's description and
the skills catalog, weighted by each user's UserSkill.weight.

Upgrade path: swap extract_skills_for_job's substring matching for embeddings
(pgvector) if keyword matching proves too shallow - the JobSkill/MatchScore
schema doesn't need to change for that, just how confidence/score are computed.
"""

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.skill import Skill, JobSkill
from app.models.user import User, UserSkill
from app.models.match_score import MatchScore


def extract_skills_for_job(db: Session, job: Job) -> list[JobSkill]:
    """Match the job's title+description text against the Skill catalog
    (by name or alias, case-insensitive substring match) and store JobSkill rows."""

    text = f"{job.title} {job.description or ''}".lower()
    all_skills = db.query(Skill).all()

    # Clear existing extractions for this job so re-runs don't duplicate.
    db.query(JobSkill).filter(JobSkill.job_id == job.id).delete()

    created = []
    for skill in all_skills:
        terms = [skill.name.lower()] + [a.lower() for a in (skill.aliases or [])]
        if any(term in text for term in terms):
            js = JobSkill(job_id=job.id, skill_id=skill.id, confidence=1.0)
            db.add(js)
            created.append(js)

    db.commit()
    return created


def compute_match_score(db: Session, user: User, job: Job) -> MatchScore:
    """Score = (sum of weights of overlapping skills / sum of all user skill
    weights) * 100. Simple, explainable, and a fine v1 before embeddings."""

    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    if not user_skills:
        score_value = 0.0
    else:
        user_skill_ids = {us.skill_id: us.weight for us in user_skills}
        job_skill_ids = {
            js.skill_id for js in db.query(JobSkill).filter(JobSkill.job_id == job.id).all()
        }

        overlap_weight = sum(w for sid, w in user_skill_ids.items() if sid in job_skill_ids)
        total_weight = sum(user_skill_ids.values()) or 1.0
        score_value = round((overlap_weight / total_weight) * 100, 1)

    existing = (
        db.query(MatchScore)
        .filter(MatchScore.user_id == user.id, MatchScore.job_id == job.id)
        .first()
    )
    if existing:
        existing.score = score_value
        db.commit()
        db.refresh(existing)
        return existing

    match = MatchScore(user_id=user.id, job_id=job.id, score=score_value)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def process_job_for_all_users(db: Session, job: Job) -> None:
    """Run after ingesting a job: extract its skills, then score it against
    every user so the dashboard has fresh match scores without recomputing
    on read."""

    extract_skills_for_job(db, job)
    for user in db.query(User).all():
        compute_match_score(db, user, job)