"""
Fallback scraper for company career pages that aren't on Greenhouse, Lever,
or Ashby. Uses Playwright since many career pages render listings
client-side (job-search-wale patterns bhi CSR pe depend karte hain).

There's no universal schema for a career page (har company ka HTML alag
hota hai) - isliye har company ke liye ek CSS-selector config CAREER_PAGE_CONFIGS
me add karna hoga. Bina config ke wo company scrape nahi hogi.
"""

from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

# Per-company selector config, keyed by hostname of the career page URL.
CAREER_PAGE_CONFIGS = {
    # "example.com": {
    #     "job_row": "div.job-listing",
    #     "title": "h3.job-title",
    #     "location": "span.job-location",
    #     "link": "a.job-link",  # href, may be relative
    # },
}


def get_career_page_jobs(url: str):
    from urllib.parse import urlparse

    hostname = urlparse(url).netloc
    config = CAREER_PAGE_CONFIGS.get(hostname)

    if not config:
        raise ValueError(
            f"No scraper config for {hostname}. Add one to CAREER_PAGE_CONFIGS "
            f"in app/collectors/career_pages.py before scraping this company."
        )

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_selector(config["job_row"], timeout=15000)

        rows = page.query_selector_all(config["job_row"])

        for row in rows:
            title_el = row.query_selector(config["title"])
            location_el = row.query_selector(config.get("location", ""))
            link_el = row.query_selector(config.get("link", config["title"]))

            if not title_el or not link_el:
                continue

            href = link_el.get_attribute("href") or ""
            if href.startswith("/"):
                href = urljoin(url, href)

            results.append({
                "title": title_el.inner_text().strip(),
                "location": location_el.inner_text().strip() if location_el else None,
                "job_url": href,
            })

        browser.close()

    return results