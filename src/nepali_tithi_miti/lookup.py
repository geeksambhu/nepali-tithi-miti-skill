from __future__ import annotations

from pathlib import Path

from .db import get_by_ad_date, get_by_bs_date
from .models import CalendarDay
from .parsing import parse_ymd

def lookup_by_bs_date(year: int, month: int, day: int, db_path: Path | None = None) -> CalendarDay | None:
    return get_by_bs_date(year, month, day, db_path=db_path)

def lookup_by_ad_date(year: int, month: int, day: int, db_path: Path | None = None) -> CalendarDay | None:
    return get_by_ad_date(year, month, day, db_path=db_path)

def lookup_by_bs_string(value: str, db_path: Path | None = None) -> CalendarDay | None:
    y, m, d = parse_ymd(value)
    return lookup_by_bs_date(y, m, d, db_path=db_path)

def lookup_by_ad_string(value: str, db_path: Path | None = None) -> CalendarDay | None:
    y, m, d = parse_ymd(value)
    return lookup_by_ad_date(y, m, d, db_path=db_path)
