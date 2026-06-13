from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Confidence = Literal["high", "medium", "low"]

@dataclass(frozen=True)
class CalendarDay:
    bs_year: int
    bs_month: int
    bs_day: int
    ad_year: int
    ad_month: int
    ad_day: int
    weekday_en: str | None = None
    weekday_np: str | None = None
    tithi_np: str | None = None
    tithi_en: str | None = None
    paksha: str | None = None
    panchang: str | None = None
    nakshatra: str | None = None
    yoga: str | None = None
    karana: str | None = None
    festival_np: str | None = None
    festival_en: str | None = None
    holiday_type: str | None = None
    source: str | None = None
    source_url: str | None = None
    fetched_at: str | None = None
    confidence: Confidence = "medium"

    @property
    def bs_date(self) -> str:
        return f"{self.bs_year:04d}-{self.bs_month:02d}-{self.bs_day:02d}"

    @property
    def ad_date(self) -> str:
        return f"{self.ad_year:04d}-{self.ad_month:02d}-{self.ad_day:02d}"

@dataclass(frozen=True)
class DateConversionResult:
    input_date: str
    output_date: str
    source: str
    confidence: Confidence
    note: str | None = None
