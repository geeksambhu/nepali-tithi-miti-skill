from __future__ import annotations

from datetime import date

from .constants import ASCII_DIGITS, DEVANAGARI_DIGITS

def to_devanagari_digits(value: str | int) -> str:
    return str(value).translate(DEVANAGARI_DIGITS)

def to_ascii_digits(value: str) -> str:
    return value.translate(ASCII_DIGITS)

def parse_ymd(value: str) -> tuple[int, int, int]:
    normalized = to_ascii_digits(value.strip()).replace("/", "-")
    parts = normalized.split("-")
    if len(parts) != 3:
        raise ValueError(f"Expected YYYY-MM-DD, got: {value!r}")
    return tuple(map(int, parts))  # type: ignore[return-value]

def parse_ad_date(value: str) -> date:
    y, m, d = parse_ymd(value)
    return date(y, m, d)
