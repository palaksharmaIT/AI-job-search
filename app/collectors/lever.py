import requests


def get_lever_jobs(site_slug: str):
    url = f"https://api.lever.co/v0/postings/{site_slug}?mode=json"

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    return data