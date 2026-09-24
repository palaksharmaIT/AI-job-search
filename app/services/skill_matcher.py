import re


CANDIDATE_SKILLS = [
    "python",
    "fastapi",
    "django",
    "sql",
    "postgresql",
    "rest api",
    "machine learning",
    "artificial intelligence",
    "ai",
    "langchain",
    "langgraph",
]


def extract_skills(description: str):
    description = description.lower()

    matched_skills = []

    for skill in CANDIDATE_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, description):
            matched_skills.append(skill)

    return matched_skills


def calculate_match_score(job_description: str):
    matched_skills = extract_skills(job_description)

    total_skills = len(CANDIDATE_SKILLS)

    score = round(
        (len(matched_skills) / total_skills) * 100
    )

    return {
        "matched_skills": matched_skills,
        "match_score": score,
    }