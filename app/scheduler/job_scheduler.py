"""
Automatic polling scheduler using APScheduler (in-process, no extra
infrastructure needed). Runs inside the FastAPI process.

For now, sources are a hardcoded list below (SOURCES_TO_POLL) rather than
pulled from the Source DB table - we'll wire that up once there's a route
to create/manage Source rows. Add your own board tokens/site slugs here.
"""

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.job_normalizer import (
    import_greenhouse_jobs,
    import_lever_jobs,
    import_ashby_jobs,
)

# Edit this list with the companies you want to track.
# type: "greenhouse" -> identifier is the board token
# type: "lever"      -> identifier is the site slug, company_name required
# type: "ashby"      -> identifier is the org slug, company_name required
SOURCES_TO_POLL = [
    # {"type": "greenhouse", "identifier": "stripe"},
    # {"type": "lever", "identifier": "netflix", "company_name": "Netflix"},
    # {"type": "ashby", "identifier": "notion", "company_name": "Notion"},
]


def poll_all_sources():
    print("[scheduler] Polling configured sources...")

    for source in SOURCES_TO_POLL:
        try:
            if source["type"] == "greenhouse":
                result = import_greenhouse_jobs(source["identifier"])
            elif source["type"] == "lever":
                result = import_lever_jobs(source["identifier"], source["company_name"])
            elif source["type"] == "ashby":
                result = import_ashby_jobs(source["identifier"], source["company_name"])
            else:
                print(f"[scheduler] Unknown source type: {source['type']}")
                continue

            print(f"[scheduler] {source['type']}/{source['identifier']}: {result}")

        except Exception as e:
            print(f"[scheduler] Failed to poll {source['type']}/{source['identifier']}: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_all_sources, "interval", minutes=30, id="poll_all_sources")
    scheduler.start()
    print("[scheduler] Started - polling every 30 minutes.")
    return scheduler