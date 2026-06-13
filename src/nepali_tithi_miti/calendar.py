from __future__ import annotations

from datetime import date, datetime
from sqlite3 import Error as SqliteError
from zoneinfo import ZoneInfo

import nepali_datetime

from .constants import NEPAL_TIMEZONE, WEEKDAYS_EN, WEEKDAYS_NP
from .lookup import lookup_by_ad_string
from .models import CalendarDay, DateConversionResult
from .parsing import parse_ad_date, parse_ymd

def get_today_ad_date() -> str:
    return datetime.now(ZoneInfo(NEPAL_TIMEZONE)).date().isoformat()

def _format_ymd(year: int, month: int, day: int) -> str:
    return f"{year:04d}-{month:02d}-{day:02d}"

def _ad_date_to_bs_date(ad_date: date) -> nepali_datetime.date:
    return nepali_datetime.date.from_datetime_date(ad_date)

def _bs_date_to_ad_date(year: int, month: int, day: int) -> date:
    return nepali_datetime.date(year, month, day).to_datetime_date()

def _calendar_day_payload(row: CalendarDay | None) -> dict[str, str | int | None]:
    if row is None:
        return {
            "tithi_np": None,
            "tithi_en": None,
            "panchang": None,
            "nakshatra": None,
            "yoga": None,
            "karana": None,
            "festival_np": None,
            "festival_en": None,
            "holiday_type": None,
            "calendar_source": None,
            "calendar_confidence": None,
        }
    return {
        "tithi_np": row.tithi_np,
        "tithi_en": row.tithi_en,
        "panchang": row.panchang,
        "nakshatra": row.nakshatra,
        "yoga": row.yoga,
        "karana": row.karana,
        "festival_np": row.festival_np,
        "festival_en": row.festival_en,
        "holiday_type": row.holiday_type,
        "calendar_source": row.source,
        "calendar_confidence": row.confidence,
    }

def get_today_nepali_date() -> dict[str, str | int | None]:
    ad_today = get_today_ad_date()
    ad_date = parse_ad_date(ad_today)
    bs_date = _ad_date_to_bs_date(ad_date)
    try:
        cached = lookup_by_ad_string(ad_today)
        cache_note = "Cache checked."
    except (OSError, SqliteError) as exc:
        cached = None
        cache_note = f"Cache unavailable: {exc}"
    weekday_index = ad_date.weekday()
    return {
        "timezone": NEPAL_TIMEZONE,
        "ad_today": ad_today,
        "bs_today": _format_ymd(bs_date.year, bs_date.month, bs_date.day),
        "bs_year": bs_date.year,
        "bs_month": bs_date.month,
        "bs_day": bs_date.day,
        "weekday_en": WEEKDAYS_EN[weekday_index],
        "weekday_np": WEEKDAYS_NP[weekday_index],
        "conversion_source": "nepali-datetime",
        "conversion_confidence": "high",
        **_calendar_day_payload(cached),
        "note": (
            "BS date converted locally with nepali-datetime. "
            "Tithi, panchang, and festival fields require verified cached API/calendar data. "
            f"{cache_note}"
        ),
    }

def ad_to_bs(ad_date: str) -> DateConversionResult:
    parsed = parse_ad_date(ad_date)
    converted = _ad_date_to_bs_date(parsed)
    return DateConversionResult(
        input_date=ad_date,
        output_date=_format_ymd(converted.year, converted.month, converted.day),
        source="nepali-datetime",
        confidence="high",
        note="Converted locally with the open-source nepali-datetime package.",
    )

def bs_to_ad(bs_date: str) -> DateConversionResult:
    year, month, day = parse_ymd(bs_date)
    converted = _bs_date_to_ad_date(year, month, day)
    return DateConversionResult(
        input_date=bs_date,
        output_date=converted.isoformat(),
        source="nepali-datetime",
        confidence="high",
        note="Converted locally with the open-source nepali-datetime package.",
    )
