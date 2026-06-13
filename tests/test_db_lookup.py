from pathlib import Path

from nepali_tithi_miti.db import upsert_calendar_days
from nepali_tithi_miti.lookup import lookup_by_ad_string, lookup_by_bs_string
from nepali_tithi_miti.models import CalendarDay

def test_db_lookup_round_trip(tmp_path: Path):
    db = tmp_path / "calendar.sqlite3"
    day = CalendarDay(
        bs_year=2083,
        bs_month=2,
        bs_day=18,
        ad_year=2026,
        ad_month=6,
        ad_day=1,
        tithi_np="अधिक जेठ कृष्ण प्रतिपदा",
        source="test",
    )
    assert upsert_calendar_days([day], db_path=db) == 1
    assert lookup_by_bs_string("2083-02-18", db_path=db).tithi_np == "अधिक जेठ कृष्ण प्रतिपदा"
    assert lookup_by_ad_string("2026-06-01", db_path=db).bs_year == 2083
