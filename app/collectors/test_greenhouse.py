from app.collectors.greenhouse import get_greenhouse_jobs


jobs = get_greenhouse_jobs("YOUR_BOARD_TOKEN")

print(f"Total jobs: {len(jobs)}")

for job in jobs[:5]:
    print("ID:", job.get("id"))
    print("Title:", job.get("title"))
    print("Location:", job.get("location", {}).get("name"))
    print("URL:", job.get("absolute_url"))
    print("-" * 50)