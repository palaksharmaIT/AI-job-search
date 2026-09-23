import requests


def get_greenhouse_jobs(board_token: str):
    url = (
        f"https://boards-api.greenhouse.io/v1/boards/"
        f"{board_token}/jobs?content=true"
    )

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    return data.get("jobs", [])