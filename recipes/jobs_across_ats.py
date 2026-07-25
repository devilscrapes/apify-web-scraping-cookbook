"""Pull job postings across every major ATS platform into one CSV.

Runs the Devil Scrapes keyless-ATS Actors — Workday, SmartRecruiters, Workable,
Teamtailor, and the combined Greenhouse/Lever/Ashby feed — and merges their
normalized rows. Each Actor talks to the platform's own public JSON feed, so no
API keys for the target sites are needed.

Actors:
  https://apify.com/DevilScrapes/workday-jobs-scraper
  https://apify.com/DevilScrapes/smartrecruiters-jobs-scraper
  https://apify.com/DevilScrapes/workable-jobs-scraper
  https://apify.com/DevilScrapes/teamtailor-jobs-scraper
  https://apify.com/DevilScrapes/multi-ats-jobs-scraper

Docs: https://apify.com/DevilScrapes
"""
from __future__ import annotations

import csv
import sys

from apify_client import ApifyClient

# Each entry: (actor slug, run input). Edit the company handles to your targets.
JOBS_ACTORS = [
    ("DevilScrapes/workday-jobs-scraper", {"companies": ["nvidia"]}),
    ("DevilScrapes/smartrecruiters-jobs-scraper", {"companies": ["Square"]}),
    ("DevilScrapes/workable-jobs-scraper", {"companies": ["remotebase"]}),
    ("DevilScrapes/teamtailor-jobs-scraper", {"companies": ["oatly", "storytel"]}),
    ("DevilScrapes/multi-ats-jobs-scraper", {"companies": ["stripe"]}),
]

FIELDS = ["source", "company", "job_title", "location", "url", "date_published"]


def run(token: str) -> list[dict]:
    client = ApifyClient(token)
    rows: list[dict] = []
    for slug, run_input in JOBS_ACTORS:
        print(f"→ running {slug} ...", file=sys.stderr)
        run_info = client.actor(slug).call(run_input=run_input)
        for item in client.dataset(run_info["defaultDatasetId"]).iterate_items():
            rows.append(
                {
                    "source": slug.split("/")[-1].replace("-jobs-scraper", ""),
                    "company": item.get("company") or item.get("company_name"),
                    "job_title": item.get("job_title") or item.get("title"),
                    "location": item.get("location_locality") or item.get("location"),
                    "url": item.get("job_url") or item.get("url"),
                    "date_published": item.get("date_published"),
                }
            )
    return rows


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python jobs_across_ats.py <APIFY_API_TOKEN>")
    rows = run(sys.argv[1])
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    print(f"\n{len(rows)} postings across {len(JOBS_ACTORS)} ATS platforms", file=sys.stderr)


if __name__ == "__main__":
    main()
