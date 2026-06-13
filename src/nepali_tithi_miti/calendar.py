from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from .constants import NEPAL_TIMEZONE
from .models import DateConversionResult

def get_today_ad_date() -> str:
    return datetime.now(ZoneInfo(NEPAL_TIMEZONE)).date().isoformat()

def get_today_nepali_date() -> dict[str, str | None]:
    ad_today = get_today_ad_date()
    return {
        "timezone": NEPAL_TIMEZONE,
        "ad_today": ad_today,
        "bs_today": None,
        "note": "Exact BS date requires a configured conversion library or cached calendar record.",
    }

def ad_to_bs(ad_date: str) -> DateConversionResult:
    return DateConversionResult(
        input_date=ad_date,
        output_date="unavailable",
        source="not_configured",
        confidence="low",
        note="AD to BS conversion library is not configured yet. Do not approximate.",
    )

def bs_to_ad(bs_date: str) -> DateConversionResult:
    return DateConversionResult(
        input_date=bs_date,
        output_date="unavailable",
        source="not_configured",
        confidence="low",
        note="BS to AD conversion library is not configured yet. Do not approximate.",
    )
