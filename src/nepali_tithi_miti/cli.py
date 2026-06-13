from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import typer
from rich.console import Console

from .calendar import ad_to_bs, bs_to_ad, get_today_nepali_date
from .db import init_db, upsert_calendar_days
from .lookup import lookup_by_ad_string, lookup_by_bs_string
from .models import CalendarDay

app = typer.Typer(help="Nepali tithi/miti calendar CLI")
console = Console()

def _print_json(obj: object) -> None:
    payload = asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj
    console.print_json(json.dumps(payload, ensure_ascii=False, default=str))

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
