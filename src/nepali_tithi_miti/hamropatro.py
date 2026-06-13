from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from .models import CalendarDay

BASE_URL = "https://www.hamropatro.com/calendar/{year}/{month}"
DEFAULT_USER_AGENT = "NepaliTithiMitiSkill/0.1 (+https://github.com/geeksambhu/nepali-tithi-miti-skill)"

def build_calendar_url(bs_year: int, bs_month: int) -> str:
    return BASE_URL.format(year=bs_year, month=bs_month)

def fetch_month_html(bs_year: int, bs_month: int, *, timeout: int = 20) -> str:
    """Fetch one calendar month.

    Use only for explicit cache-building when allowed by the site terms/robots.
    Do not use this per live user request.
    """
    response = requests.get(
        build_calendar_url(bs_year, bs_month),
        headers={"User-Agent": DEFAULT_USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text

def parse_month_html(html: str, bs_year: int, bs_month: int, source_url: str) -> list[CalendarDay]:
    """Parse calendar HTML after selectors are verified.

    Placeholder parser intentionally returns no records until you inspect current HTML,
    define selectors, and add tests with saved fixtures.
    """
    soup = BeautifulSoup(html, "html.parser")
    _raw_text = [cell.get_text(" ", strip=True) for cell in soup.select("td, .calendar-day, .date-cell")]
    _ = (bs_year, bs_month, source_url, datetime.now(timezone.utc).isoformat(), _raw_text)
    return []

def ingest_month(bs_year: int, bs_month: int) -> Iterable[CalendarDay]:
    url = build_calendar_url(bs_year, bs_month)
    html = fetch_month_html(bs_year, bs_month)
    return parse_month_html(html, bs_year, bs_month, url)
