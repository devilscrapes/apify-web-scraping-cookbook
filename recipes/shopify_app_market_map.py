"""Map a Shopify App Store category into a competitive pricing table.

Discovers the apps in one or more Shopify App Store categories, then flattens
each app's pricing plans into one CSV row per plan — so you can sort a whole
category by entry price, spot who is actually free vs. free-trial, and see
which competitors carry the review volume.

Two details this recipe exists to demonstrate:

  1. `price` is a STRING, not a number ("Free", "$29/month", "From $5/month").
     Shopify's own pricing UI is prose, and coercing it to a float silently
     destroys the distinction between "free forever" and "free to install,
     usage-billed". This recipe keeps the raw string and derives a separate
     nullable numeric column, so a failed parse stays visible instead of
     becoming a confident zero.

  2. `install_count` is always None. The Shopify App Store stopped exposing
     install counts publicly, so the field is present for schema stability but
     never populated. Use `review_count` as the traction proxy.

Actor:
  https://apify.com/DevilScrapes/shopify-app-store-scraper

Docs: https://apify.com/DevilScrapes
"""
from __future__ import annotations

import csv
import re
import sys

from apify_client import ApifyClient

ACTOR = "DevilScrapes/shopify-app-store-scraper"

# Category discovery returns up to 40 apps per category slug.
# Swap these for the categories you actually compete in.
CATEGORY_SLUGS = ["email-marketing", "upselling-and-cross-selling"]
MAX_ITEMS = 40

FIELDS = [
    "handle",
    "name",
    "developer",
    "category",
    "plan_name",
    "plan_price_raw",
    "plan_price_usd",
    "plan_additional_charges",
    "rating_value",
    "review_count",
    "launched_date",
    "url",
]

_MONEY = re.compile(r"\$\s*([0-9][0-9,]*(?:\.[0-9]{2})?)")


def parse_price_usd(raw: str | None) -> float | None:
    """Best-effort numeric price. Returns None when the plan isn't a plain amount.

    "Free" -> None (deliberately: it is not 0.0 in the billing sense you care
    about, and conflating them is how "free trial" gets counted as "free").
    "$29/month" -> 29.0
    "From $5/month" -> 5.0
    """
    if not raw:
        return None
    match = _MONEY.search(raw)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def run(token: str) -> list[dict]:
    client = ApifyClient(token)
    run_input = {"categorySlugs": CATEGORY_SLUGS, "maxItems": MAX_ITEMS}

    print(f"→ running {ACTOR} over {len(CATEGORY_SLUGS)} categories ...", file=sys.stderr)
    run_info = client.actor(ACTOR).call(run_input=run_input)

    rows: list[dict] = []
    for app in client.dataset(run_info["defaultDatasetId"]).iterate_items():
        plans = app.get("pricing_plans") or [{}]  # keep apps that list no plan
        for plan in plans:
            raw_price = plan.get("price")
            rows.append(
                {
                    "handle": app.get("handle"),
                    "name": app.get("name"),
                    "developer": app.get("developer"),
                    "category": app.get("category"),
                    "plan_name": plan.get("name"),
                    "plan_price_raw": raw_price,
                    "plan_price_usd": parse_price_usd(raw_price),
                    "plan_additional_charges": plan.get("additional_charges"),
                    "rating_value": app.get("rating_value"),
                    "review_count": app.get("review_count"),
                    "launched_date": app.get("launched_date"),
                    "url": app.get("url"),
                }
            )
    return rows


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python shopify_app_market_map.py <APIFY_TOKEN>")

    rows = run(sys.argv[1])

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

    priced = [r for r in rows if r["plan_price_usd"] is not None]
    print(
        f"\n{len(rows)} plan rows across {len({r['handle'] for r in rows})} apps; "
        f"{len(priced)} carry a parseable amount.",
        file=sys.stderr,
    )
    if priced:
        cheapest = min(priced, key=lambda r: r["plan_price_usd"])
        print(
            f"cheapest paid entry point: {cheapest['name']} "
            f"({cheapest['plan_name']}, {cheapest['plan_price_raw']})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
