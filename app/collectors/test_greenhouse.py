from app.collectors.greenhouse import get_greenhouse_jobs

jobs = get_greenhouse_jobs("stripe")

print(f"Total jobs: {len(jobs)}")

for job in jobs[:10]:
    print(
        f"ID: {job['id']}\n"
        f"Title: {job['title']}\n"
        f"Company: {job['company_name']}\n"
        f"Location: {job['location']['name']}\n"
        f"URL: {job['absolute_url']}\n"
        f"{'-' * 60}"
    )