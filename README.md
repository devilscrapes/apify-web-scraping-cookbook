# 🦇 Apify Web Scraping Cookbook — by Devil Scrapes

Ready-to-run recipes for pulling clean, structured data from the web using
[**Devil Scrapes** Actors on the Apify Store](https://apify.com/DevilScrapes).

Every Actor here is a self-contained scraper you call over the Apify API — no
servers, no proxies to manage, no anti-blocking to babysit. We handle the browser
fingerprints, retries, proxy rotation, and edge cases; you get JSON or CSV.

```python
# The one pattern every recipe uses
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_API_TOKEN")
run = client.actor("DevilScrapes/<actor-slug>").call(run_input={...})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row)
```

Get a free Apify token at [apify.com](https://apify.com) — every account starts
with free monthly credit, no card required.

---

## 📚 Recipe index

### Jobs & hiring intelligence (keyless ATS feeds)
Pull live job postings straight from the ATS platforms that power most company
career sites — one normalized schema across all of them.

| Recipe | Actor |
|---|---|
| Workday career sites (`*.myworkdayjobs.com`) | [workday-jobs-scraper](https://apify.com/DevilScrapes/workday-jobs-scraper) |
| SmartRecruiters employers | [smartrecruiters-jobs-scraper](https://apify.com/DevilScrapes/smartrecruiters-jobs-scraper) |
| Workable boards | [workable-jobs-scraper](https://apify.com/DevilScrapes/workable-jobs-scraper) |
| Teamtailor career sites | [teamtailor-jobs-scraper](https://apify.com/DevilScrapes/teamtailor-jobs-scraper) |
| Greenhouse + Lever + Ashby (one feed) | [multi-ats-jobs-scraper](https://apify.com/DevilScrapes/multi-ats-jobs-scraper) |
| BambooHR careers sites | [bamboohr-jobs-scraper](https://apify.com/DevilScrapes/bamboohr-jobs-scraper) |
| Recruitee boards | [recruitee-jobs-scraper](https://apify.com/DevilScrapes/recruitee-jobs-scraper) |
| Ashby boards (dedicated) | [ashby-jobs-scraper](https://apify.com/DevilScrapes/ashby-jobs-scraper) |
| Personio careers pages | [personio-jobs-scraper](https://apify.com/DevilScrapes/personio-jobs-scraper) |
| Breezy HR boards | [breezy-hr-jobs-scraper](https://apify.com/DevilScrapes/breezy-hr-jobs-scraper) |

→ Runnable example: [`recipes/jobs_across_ats.py`](recipes/jobs_across_ats.py)

### B2B lead generation
| Recipe | Actor |
|---|---|
| US healthcare providers (NPI registry) | [npi-healthcare-provider-scraper](https://apify.com/DevilScrapes/npi-healthcare-provider-scraper) |
| Shopify store leads from a domain list | [shopify-store-leads-scraper](https://apify.com/DevilScrapes/shopify-store-leads-scraper) |
| US building-permit contractor leads | [us-building-permit-leads-scraper](https://apify.com/DevilScrapes/us-building-permit-leads-scraper) |

### Marketplaces & commerce
| Recipe | Actor |
|---|---|
| Mercari US sold/completed listings | [mercari-sold-listings](https://apify.com/DevilScrapes/mercari-sold-listings) |
| Gumroad products & storefronts | [gumroad-product-scraper](https://apify.com/DevilScrapes/gumroad-product-scraper) |
| Goodreads books & reviews | [goodreads-book-reviews-scraper](https://apify.com/DevilScrapes/goodreads-book-reviews-scraper) |

### Events
| Recipe | Actor |
|---|---|
| Lu.ma public events by city/category | [luma-event-discovery](https://apify.com/DevilScrapes/luma-event-discovery) |
| Meetup events by keyword + location | [meetup-events-scraper](https://apify.com/DevilScrapes/meetup-events-scraper) |
| Every event from a Meetup group | [meetup-group-scraper](https://apify.com/DevilScrapes/meetup-group-scraper) |

### Content & market data
| Recipe | Actor |
|---|---|
| Full Substack publication archives | [substack-newsletter-scraper](https://apify.com/DevilScrapes/substack-newsletter-scraper) |
| Website tech stacks (BuiltWith alternative) | [builtwith-alternative-scraper](https://apify.com/DevilScrapes/builtwith-alternative-scraper) |
| Japan real estate (SUUMO) | [suumo-japan-real-estate](https://apify.com/DevilScrapes/suumo-japan-real-estate) |

---

## Why these Actors don't break

Every Devil Scrapes Actor ships the same defensive stack so your runs finish with
data, not empty datasets:

- **Browser TLS/H2 impersonation** — requests present a real Chrome/Firefox/Safari
  handshake, not a Python HTTP client.
- **Proxy session rotation** — a fresh residential exit IP on every block.
- **Exponential-backoff retries** on 408/429/5xx, honouring `Retry-After`.
- **Honest partial results** — a clear status message on partial runs; never a green
  status hiding an empty dataset.

## Browse the full fleet

70+ Actors and counting at **[apify.com/DevilScrapes](https://apify.com/DevilScrapes)**.
Missing a target? Open an issue here and we'll look at building it.

## License

MIT — the recipes in this repo are yours to copy and adapt.
