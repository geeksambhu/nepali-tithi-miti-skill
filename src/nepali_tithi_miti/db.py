from __future__ import annotations

import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .config import get_db_path
from .models import CalendarDay

SCHEMA = """
CREATE TABLE IF NOT EXISTS nepali_calendar_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bs_year INTEGER NOT NULL,
    bs_month INTEGER NOT NULL,
    bs_day INTEGER NOT NULL,
    ad_year INTEGER NOT NULL,
    ad_month INTEGER NOT NULL,
    ad_day INTEGER NOT NULL,
    weekday_en TEXT,
    weekday_np TEXT,
    tithi_np TEXT,
    tithi_en TEXT,
    paksha TEXT,
    panchang TEXT,
    nakshatra TEXT,
    yoga TEXT,
    karana TEXT,
    festival_np TEXT,
    festival_en TEXT,
    holiday_type TEXT,
    source TEXT,
    source_url TEXT,
    fetched_at TEXT,
    confidence TEXT NOT NULL DEFAULT 'medium',
    UNIQUE(bs_year, bs_month, bs_day),
    UNIQUE(ad_year, ad_month, ad_day)
);
CREATE INDEX IF NOT EXISTS idx_nepali_calendar_bs
ON nepali_calendar_days(bs_year, bs_month, bs_day);
CREATE INDEX IF NOT EXISTS idx_nepali_calendar_ad
ON nepali_calendar_days(ad_year, ad_month, ad_day);
"""

def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)

def upsert_calendar_days(days: Iterable[CalendarDay], db_path: Path | None = None) -> int:
    init_db(db_path)
    rows = list(days)
    if not rows:
        return 0
    fields = list(asdict(rows[0]).keys())
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)
    update_columns = ", ".join(
        [f"{f}=excluded.{f}" for f in fields if f not in {"bs_year", "bs_month", "bs_day"}]
    )
    sql = f"""
    INSERT INTO nepali_calendar_days ({columns})
    VALUES ({placeholders})
    ON CONFLICT(bs_year, bs_month, bs_day)
    DO UPDATE SET {update_columns}
    """
    with connect(db_path) as conn:
        conn.executemany(sql, [[getattr(day, f) for f in fields] for day in rows])
    return len(rows)

def _row_to_calendar_day(row: sqlite3.Row | None) -> CalendarDay | None:
    if row is None:
        return None
    data = dict(row)
    data.pop("id", None)
    return CalendarDay(**data)

def get_by_bs_date(year: int, month: int, day: int, db_path: Path | None = None) -> CalendarDay | None:
    init_db(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM nepali_calendar_days WHERE bs_year=? AND bs_month=? AND bs_day=?",
            (year, month, day),
        ).fetchone()
    return _row_to_calendar_day(row)

def get_by_ad_date(year: int, month: int, day: int, db_path: Path | None = None) -> CalendarDay | None:
    init_db(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM nepali_calendar_days WHERE ad_year=? AND ad_month=? AND ad_day=?",
            (year, month, day),
        ).fetchone()
    return _row_to_calendar_day(row)
