import logging
import sys

import pandas as pd
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import EventData, Events
from linkedin_jobs_scraper.filters import (ExperienceLevelFilters,
                                           OnSiteOrRemoteFilters,
                                           RelevanceFilters, TimeFilters,
                                           TypeFilters)
from linkedin_jobs_scraper.query import Query, QueryFilters, QueryOptions

MAX_THREADS = 1
PAGE_LOAD_TIMEOUT_IN_SECONDS = 40

def main():
    logging.basicConfig(level=logging.INFO)
    sheet_data = []

    def on_successfully_processed_job(data: EventData):
        sheet_data.append({
            "title": data.title,
            "company":  data.company,
            "company_link": data.company_link,
            "date": data.date,
            "link": data.link,
            "insights": data.insights,
            "description": data.description
        })

    def on_error(error):
        print("[ON_ERROR]", error)

    def on_end():
        print("[ON_END]")

    scraper = LinkedinScraper(
        chrome_executable_path=None,
        chrome_options=None,
        headless=True,
        max_workers=MAX_THREADS,
        slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=PAGE_LOAD_TIMEOUT_IN_SECONDS
    )

    scraper.on(Events.DATA, on_successfully_processed_job)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    query = sys.argv.pop()
    queries = [
        Query(
            query=query,
            options=QueryOptions(
                locations=["Brazil"],
                apply_link=True,
                skip_promoted_jobs=False,
                page_offset=0,
                limit=1000,
                filters=QueryFilters(
                    company_jobs_url=None,
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                    experience=[ExperienceLevelFilters.ENTRY_LEVEL]
                )
            )
        ),
    ]

    scraper.run(queries)

    df = pd.DataFrame(sheet_data)
    df.to_csv("linkedinjobs.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()