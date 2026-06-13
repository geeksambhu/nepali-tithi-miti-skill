from __future__ import annotations

import os
from pathlib import Path

def default_data_dir() -> Path:
    return Path.home() / ".nepali_tithi_miti"

def get_db_path() -> Path:
    override = os.getenv("NEPALI_TITHI_MITI_DB")
    if override:
        return Path(override).expanduser()
    return default_data_dir() / "calendar.sqlite3"
