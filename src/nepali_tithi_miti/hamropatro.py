from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from .constants import NEPALI_MONTHS_EN, NEPALI_MONTHS_NP, WEEKDAYS_NP
from .models import CalendarDay
from .parsing import to_ascii_digits

BASE_URL = "https://www.hamropatro.com/calendar/{year}/{month}"
NEPALI_CALENDAR_URL = "https://www.nepalicalendar.com/"
NEPALI_PATRO_URL = "https://nepalipatro.com.np/"
NEPALI_PATRO_PANCHANGA_API_URL = "https://api.nepalipatro.com.np/fetch/panchanga"
DEFAULT_USER_AGENT = "NepaliTithiMitiSkill/0.1 (+https://github.com/geeksambhu/nepali-tithi-miti-skill)"
ENGLISH_MONTH_NUMBERS = {
    "January": 1,
    "Jan": 1,
    "February": 2,
    "Feb": 2,
    "March": 3,
    "Mar": 3,
    "April": 4,
    "Apr": 4,
    "May": 5,
    "June": 6,
    "Jun": 6,
    "July": 7,
    "Jul": 7,
    "August": 8,
    "Aug": 8,
    "September": 9,
    "Sep": 9,
    "October": 10,
    "Oct": 10,
    "November": 11,
    "Nov": 11,
    "December": 12,
    "Dec": 12,
}
NEPALI_MONTH_NUMBERS = {name: index for index, name in enumerate(NEPALI_MONTHS_NP, start=1)}
NEPALI_CALENDAR_MONTH_NUMBERS = {
    "Bhaishak": 1,
    "Baisakh": 1,
    "Baishakh": 1,
    "Jestha": 2,
    "Ashadh": 3,
    "Shrawan": 4,
    "Bhadra": 5,
    "Ashwin": 6,
    "Kartik": 7,
    "Mangsir": 8,
    "Poush": 9,
    "Magh": 10,
    "Falgun": 11,
    "Chaitra": 12,
}

def build_calendar_url(bs_year: int, bs_month: int) -> str:
    return BASE_URL.format(year=bs_year, month=bs_month)

def _fetch_url(url: str, *, timeout: int = 20) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text

def fetch_month_html(bs_year: int, bs_month: int, *, timeout: int = 20) -> str:
    """Fetch one calendar month.

    Use only for explicit cache-building when allowed by the site terms/robots.
    Do not use this per live user request.
    """
    return _fetch_url(build_calendar_url(bs_year, bs_month), timeout=timeout)

def fetch_nepali_calendar_html(*, timeout: int = 20) -> str:
    """Fetch the current NepalCalendar/PrabhuPatro page for explicit user-requested lookup."""
    return _fetch_url(NEPALI_CALENDAR_URL, timeout=timeout)

def fetch_nepali_patro_html(*, timeout: int = 20) -> str:
    """Fetch the current NepaliPatro page for explicit user-requested lookup."""
    return _fetch_url(NEPALI_PATRO_URL, timeout=timeout)

def fetch_nepali_patro_panchanga_api(ad_date: date, time_value: str, *, timeout: int = 20) -> dict | None:
    """Attempt NepaliPatro's panchanga API.

    The endpoint may return an encrypted payload instead of plain JSON. In that case this returns
    None and callers should fall back to public page parsing.
    """
    response = requests.post(
        NEPALI_PATRO_PANCHANGA_API_URL,
        headers={
            "accept": "application/json, text/plain, */*",
            "origin": NEPALI_PATRO_URL.rstrip("/"),
            "referer": NEPALI_PATRO_URL,
            "user-agent": DEFAULT_USER_AGENT,
        },
        files={
            "year": (None, f"{ad_date.year:04d}"),
            "month": (None, f"{ad_date.month:02d}"),
            "day": (None, f"{ad_date.day:02d}"),
            "time": (None, time_value),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError:
        return None
    if isinstance(payload, dict) and {"iv", "value", "mac"}.issubset(payload):
        return None
    return payload if isinstance(payload, dict) else None

def fetch_hamropatro_home_html(*, timeout: int = 20) -> str:
    """Fetch Hamro Patro home page for explicit user-requested today lookup."""
    return _fetch_url("https://www.hamropatro.com/", timeout=timeout)

def _text_lines(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [line.strip() for line in soup.get_text("\n").splitlines() if line.strip()]

def _parse_hamro_ad_date(value: str) -> date:
    normalized = value.replace(",", "").strip()
    for fmt in ("%B %d %Y", "%b %d %Y"):
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported AD date format: {value!r}")

def _parse_bs_heading(value: str) -> tuple[int, int, int, str | None] | None:
    match = re.match(r"^([०-९0-9]+)\s+(\S+)\s+([०-९0-9]+),\s*(.+)$", value)
    if not match:
        return None
    day_text, month_name, year_text, weekday_np = match.groups()
    month = NEPALI_MONTH_NUMBERS.get(month_name)
    if month is None:
        return None
    return int(to_ascii_digits(year_text)), month, int(to_ascii_digits(day_text)), weekday_np

def _split_panchang(value: str) -> tuple[str | None, str | None, str | None, str | None]:
    if not value.startswith("पञ्चाङ्ग:"):
        return None, None, None, None
    panchang = value.removeprefix("पञ्चाङ्ग:").strip()
    if not panchang:
        return None, None, None, None
    parts = panchang.split()
    yoga = parts[0] if len(parts) > 0 else None
    karana = parts[1] if len(parts) > 1 else None
    nakshatra = " ".join(parts[2:]) if len(parts) > 2 else None
    return panchang, nakshatra, yoga, karana

def _is_probable_tithi(value: str) -> bool:
    markers = {
        "प्रतिपदा",
        "द्वितीया",
        "तृतिया",
        "तृतीया",
        "चतुर्थी",
        "पञ्चमी",
        "षष्ठी",
        "सप्तमी",
        "अष्टमी",
        "नवमी",
        "दशमी",
        "एकादशी",
        "द्वादशी",
        "त्रयोदशी",
        "चतुर्दशी",
        "औंसी",
        "अमावस्या",
        "पूर्णिमा",
    }
    return any(marker in value for marker in markers)

def _find_ad_date(lines: list[str]) -> date | None:
    for line in lines:
        try:
            return _parse_hamro_ad_date(line)
        except ValueError:
            continue
    return None

def _calendar_day_from_hamro_block(
    *,
    bs_year: int,
    bs_month: int,
    bs_day: int,
    weekday_np: str | None,
    ad_date: date,
    lines: list[str],
    source: str,
    source_url: str,
    confidence: str = "medium",
) -> CalendarDay | None:
    tithi_np = next((line for line in lines if _is_probable_tithi(line)), None)
    panchang_line = None
    for index, line in enumerate(lines):
        if not line.startswith("पञ्चाङ्ग:"):
            continue
        panchang_line = line
        if line.strip() == "पञ्चाङ्ग:" and index + 1 < len(lines):
            panchang_line = f"{line} {lines[index + 1]}"
        break
    panchang, nakshatra, yoga, karana = (
        _split_panchang(panchang_line) if panchang_line else (None, None, None, None)
    )
    if tithi_np is None and panchang is None:
        return None
    return CalendarDay(
        bs_year=bs_year,
        bs_month=bs_month,
        bs_day=bs_day,
        ad_year=ad_date.year,
        ad_month=ad_date.month,
        ad_day=ad_date.day,
        weekday_en=ad_date.strftime("%A"),
        weekday_np=weekday_np,
        tithi_np=tithi_np,
        panchang=panchang,
        nakshatra=nakshatra,
        yoga=yoga,
        karana=karana,
        source=source,
        source_url=source_url,
        fetched_at=datetime.now(timezone.utc).isoformat(),
        confidence=confidence,  # type: ignore[arg-type]
    )

def parse_month_html(html: str, bs_year: int, bs_month: int, source_url: str) -> list[CalendarDay]:
    """Parse Hamro Patro month HTML into cacheable calendar records."""
    lines = _text_lines(html)
    fetched_at = datetime.now(timezone.utc).isoformat()
    days: list[CalendarDay] = []

    for index, line in enumerate(lines):
        parsed_bs = _parse_bs_heading(line)
        if parsed_bs is None:
            continue
        parsed_year, parsed_month, parsed_day, weekday_np = parsed_bs
        if parsed_year != bs_year or parsed_month != bs_month:
            continue
        if index + 2 >= len(lines):
            continue
        try:
            ad_date = _parse_hamro_ad_date(lines[index + 1])
        except ValueError:
            continue
        day = _calendar_day_from_hamro_block(
            bs_year=parsed_year,
            bs_month=parsed_month,
            bs_day=parsed_day,
            weekday_np=weekday_np,
            ad_date=ad_date,
            lines=lines[index + 2 : index + 8],
            source="hamropatro",
            source_url=source_url,
        )
        if day is not None:
            days.append(day)
    return days

def parse_hamropatro_home_today(html: str) -> CalendarDay | None:
    """Parse Hamro Patro's top today block.

    Expected block:
    ३० जेठ २०८३, शनिवार
    अधिक जेठ कृष्ण त्रयोदशी
    पञ्चाङ्ग: सुकर्मा गर कृत्तिका
    दिउँसोको १२:५७:१३
    Jun 13, 2026
    """
    lines = _text_lines(html)
    fetched_at = datetime.now(timezone.utc).isoformat()
    for index, line in enumerate(lines):
        parsed_bs = _parse_bs_heading(line)
        if parsed_bs is None:
            continue
        block = lines[index + 1 : index + 12]
        ad_date = _find_ad_date(block)
        if ad_date is None:
            continue
        bs_year, bs_month, bs_day, weekday_np = parsed_bs
        return _calendar_day_from_hamro_block(
            bs_year=bs_year,
            bs_month=bs_month,
            bs_day=bs_day,
            weekday_np=weekday_np,
            ad_date=ad_date,
            lines=block,
            source="hamropatro-home",
            source_url="https://www.hamropatro.com/",
        )
    return None

def ingest_month(bs_year: int, bs_month: int) -> Iterable[CalendarDay]:
    url = build_calendar_url(bs_year, bs_month)
    html = fetch_month_html(bs_year, bs_month)
    return parse_month_html(html, bs_year, bs_month, url)

def scrape_hamropatro_day(ad_date: date, bs_year: int, bs_month: int) -> CalendarDay | None:
    home_day = parse_hamropatro_home_today(fetch_hamropatro_home_html())
    if home_day is not None and home_day.ad_date == ad_date.isoformat():
        return home_day
    url = build_calendar_url(bs_year, bs_month)
    for day in parse_month_html(fetch_month_html(bs_year, bs_month), bs_year, bs_month, url):
        if day.ad_date == ad_date.isoformat():
            return day
    return None

def _parse_nepali_calendar_header(lines: list[str]) -> tuple[int, int, int, list[int]] | None:
    bs_month = bs_year = ad_year = None
    ad_months: list[int] = []
    for line in lines[:20]:
        month_match = re.match(r"^([A-Za-z]+)\s+([0-9]{4})$", line)
        if month_match:
            bs_month = NEPALI_CALENDAR_MONTH_NUMBERS.get(month_match.group(1))
            bs_year = int(month_match.group(2))
            continue
        ad_match = re.match(r"^([A-Za-z]+)/([A-Za-z]+)\s+([0-9]{4})$", line)
        if ad_match:
            ad_months = [ENGLISH_MONTH_NUMBERS[ad_match.group(1)], ENGLISH_MONTH_NUMBERS[ad_match.group(2)]]
            ad_year = int(ad_match.group(3))
    if bs_month is None or bs_year is None or ad_year is None or not ad_months:
        return None
    return bs_year, bs_month, ad_year, ad_months

def parse_nepali_calendar_current_html(html: str, target_ad_date: date) -> CalendarDay | None:
    """Parse the current NepalCalendar/PrabhuPatro page for a target AD date.

    The page exposes BS day, AD day, and tithi for the current visible month. It does not expose
    full panchang fields in the month grid, so those remain unavailable.
    """
    lines = _text_lines(html)
    header = _parse_nepali_calendar_header(lines)
    if header is None:
        return None
    bs_year, bs_month, ad_year, ad_months = header
    current_ad_month = ad_months[0]
    fetched_at = datetime.now(timezone.utc).isoformat()

    for index, line in enumerate(lines):
        normalized = to_ascii_digits(line)
        if not normalized.isdigit() or index + 2 >= len(lines):
            continue
        bs_day = int(normalized)
        ad_token = lines[index + 1].replace("\xa0", " ")
        ad_parts = ad_token.split()
        if len(ad_parts) == 2 and ad_parts[0] in ENGLISH_MONTH_NUMBERS:
            current_ad_month = ENGLISH_MONTH_NUMBERS[ad_parts[0]]
            ad_day = int(ad_parts[1])
        elif ad_token.isdigit():
            ad_day = int(ad_token)
        else:
            continue
        try:
            parsed_ad = date(ad_year, current_ad_month, ad_day)
        except ValueError:
            continue
        if parsed_ad != target_ad_date:
            continue
        weekday_index = parsed_ad.weekday()
        return CalendarDay(
            bs_year=bs_year,
            bs_month=bs_month,
            bs_day=bs_day,
            ad_year=parsed_ad.year,
            ad_month=parsed_ad.month,
            ad_day=parsed_ad.day,
            weekday_en=parsed_ad.strftime("%A"),
            weekday_np=WEEKDAYS_NP[weekday_index],
            tithi_np=lines[index + 2],
            source="nepalicalendar",
            source_url=NEPALI_CALENDAR_URL,
            fetched_at=fetched_at,
            confidence="low",
        )
    return None

def scrape_nepali_calendar_today(ad_date: date) -> CalendarDay | None:
    return parse_nepali_calendar_current_html(fetch_nepali_calendar_html(), ad_date)

def parse_nepali_patro_today_html(html: str, target_ad_date: date) -> CalendarDay | None:
    """Parse NepaliPatro's public today block."""
    lines = _text_lines(html)
    fetched_at = datetime.now(timezone.utc).isoformat()
    for index, line in enumerate(lines):
        match = re.match(r"^([०-९0-9]+)\s+(.+)$", line)
        if match is None or index + 4 >= len(lines):
            continue
        ad_line = lines[index + 1].replace(",", "")
        try:
            ad_date = datetime.strptime(ad_line, "%d %B %Y").date()
        except ValueError:
            continue
        if ad_date != target_ad_date:
            continue
        bs_header = lines[index + 2].replace(",", "")
        bs_match = re.match(r"^(.+)\s+([०-९0-9]+)$", bs_header)
        if bs_match is None:
            continue
        month_name, year_text = bs_match.groups()
        month = NEPALI_MONTH_NUMBERS.get(month_name)
        if month is None:
            continue
        return CalendarDay(
            bs_year=int(to_ascii_digits(year_text)),
            bs_month=month,
            bs_day=int(to_ascii_digits(match.group(1))),
            ad_year=ad_date.year,
            ad_month=ad_date.month,
            ad_day=ad_date.day,
            weekday_en=ad_date.strftime("%A"),
            weekday_np=match.group(2),
            tithi_np=lines[index + 4],
            source="nepalipatro",
            source_url=NEPALI_PATRO_URL,
            fetched_at=fetched_at,
            confidence="medium",
        )
    return None

def scrape_nepali_patro_today(ad_date: date, time_value: str) -> CalendarDay | None:
    # Try the panchanga API first. If the service returns encrypted data, use the public page.
    payload = fetch_nepali_patro_panchanga_api(ad_date, time_value)
    if payload:
        # The public API shape is not stable/documented; keep this conservative and rely on
        # page parsing unless plain, recognizable fields are returned.
        tithi = payload.get("tithi") or payload.get("tithi_np") or payload.get("tithiName")
        if tithi:
            base = parse_nepali_patro_today_html(fetch_nepali_patro_html(), ad_date)
            if base is not None:
                return CalendarDay(**{**base.__dict__, "tithi_np": str(tithi), "source": "nepalipatro-api"})
    return parse_nepali_patro_today_html(fetch_nepali_patro_html(), ad_date)
