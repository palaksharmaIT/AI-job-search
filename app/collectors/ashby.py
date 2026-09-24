import requests


def get_ashby_jobs(org_slug: str):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org_slug}"

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    return data.get("jobs", [])