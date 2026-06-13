from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import typer
from requests import RequestException
from rich.console import Console

from .calendar import ad_to_bs, bs_to_ad, get_today_nepali_date
from .constants import NEPAL_TIMEZONE
from .db import init_db, upsert_calendar_days
from .hamropatro import (
    scrape_hamropatro_day,
    scrape_nepali_calendar_today,
    scrape_nepali_patro_today,
)
from .lookup import lookup_by_ad_string, lookup_by_bs_string
from .models import CalendarDay
from .parsing import parse_ad_date, parse_ymd

app = typer.Typer(help="Nepali tithi/miti calendar CLI")
console = Console()

def _print_json(obj: object) -> None:
    payload = asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj
    console.print_json(json.dumps(payload, ensure_ascii=False, default=str))

def datetime_now_time() -> str:
    return datetime.now(ZoneInfo(NEPAL_TIMEZONE)).strftime("%H:%M:%S")

def _scrape_for_ad_date(ad_date_text: str, source: str) -> tuple[CalendarDay | None, list[str]]:
    ad_date = parse_ad_date(ad_date_text)
    bs_year, bs_month, _ = parse_ymd(ad_to_bs(ad_date_text).output_date)
    row = None
    failures: list[str] = []
    normalized_source = source.lower().strip()

    if normalized_source in {"all", "hamropatro"}:
        try:
            row = scrape_hamropatro_day(ad_date, bs_year, bs_month)
        except RequestException as exc:
            failures.append(f"hamropatro: {exc}")
    if row is None and normalized_source in {"all", "nepalipatro", "nepali-patro"}:
        try:
            row = scrape_nepali_patro_today(ad_date, datetime_now_time())
        except RequestException as exc:
            failures.append(f"nepalipatro: {exc}")
    if row is None and normalized_source in {"all", "nepalicalendar", "nepali-calendar"}:
        try:
            row = scrape_nepali_calendar_today(ad_date)
        except RequestException as exc:
            failures.append(f"nepalicalendar: {exc}")

    return row, failures

@app.command("today")
def today() -> None:
    _print_json(get_today_nepali_date())

@app.command("ad-to-bs")
def cli_ad_to_bs(ad_date: str) -> None:
    _print_json(ad_to_bs(ad_date))

@app.command("bs-to-ad")
def cli_bs_to_ad(bs_date: str) -> None:
    _print_json(bs_to_ad(bs_date))

@app.command("init-db")
def cli_init_db() -> None:
    init_db()
    console.print("[green]Initialized database.[/green]")

@app.command("lookup-bs")
def cli_lookup_bs(bs_date: str) -> None:
    row = lookup_by_bs_string(bs_date)
    if row is None:
        console.print("[yellow]No cached calendar data found for this BS date.[/yellow]")
        raise typer.Exit(code=1)
    _print_json(row)

@app.command("lookup-ad")
def cli_lookup_ad(ad_date: str) -> None:
    row = lookup_by_ad_string(ad_date)
    if row is None:
        console.print("[yellow]No cached calendar data found for this AD date.[/yellow]")
        raise typer.Exit(code=1)
    _print_json(row)

@app.command("seed-sample-data")
def seed_sample_data(path: Path = Path("data/sample_calendar_days.json")) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    days = [CalendarDay(**item) for item in payload]
    count = upsert_calendar_days(days)
    console.print(f"[green]Seeded {count} calendar day(s).[/green]")

@app.command("scrape-today")
def scrape_today(
    source: str = typer.Option(
        "all",
        help="Source to try: all, hamropatro, nepalipatro, or nepalicalendar.",
    ),
    cache: bool = typer.Option(True, help="Save scraped result to the local SQLite cache."),
) -> None:
    today_payload = get_today_nepali_date()
    row, failures = _scrape_for_ad_date(str(today_payload["ad_today"]), source)

    if row is None:
        console.print("[yellow]No scraped calendar data found for today.[/yellow]")
        for failure in failures:
            console.print(f"[yellow]{failure}[/yellow]")
        raise typer.Exit(code=1)

    if cache:
        upsert_calendar_days([row])
    _print_json(row)

@app.command("scrape-date")
def scrape_date(
    ad_date: str,
    source: str = typer.Option(
        "all",
        help="Source to try: all, hamropatro, nepalipatro, or nepalicalendar.",
    ),
    cache: bool = typer.Option(True, help="Save scraped result to the local SQLite cache."),
) -> None:
    row, failures = _scrape_for_ad_date(ad_date, source)

    if row is None:
        console.print(f"[yellow]No scraped calendar data found for {ad_date}.[/yellow]")
        for failure in failures:
            console.print(f"[yellow]{failure}[/yellow]")
        raise typer.Exit(code=1)

    if cache:
        upsert_calendar_days([row])
    _print_json(row)
