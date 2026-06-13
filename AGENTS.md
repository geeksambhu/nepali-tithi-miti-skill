# Nepali Tithi Miti Agent Instructions

Use `skills/nepali-tithi-miti/SKILL.md` for Nepali Bikram Sambat, miti, tithi, panchang, festival, and AD/BS conversion requests.

## Local Setup

Install and run through `uv`:

```bash
uv sync --extra dev
uv run nepali-tithi today
uv run pytest
```

## Calendar Rules

1. Use `nepali-datetime` through the local `nepali-tithi` CLI for AD/BS conversion.
2. Do not guess tithi, nakshatra, yoga, karana, panchang, or festival dates.
3. Use verified cached calendar/API data for tithi, panchang, and festival fields.
4. Use `Asia/Kathmandu` for today/current-time requests.
5. If verified cache/API data is missing, return the BS date from conversion and mark tithi/panchang fields unavailable.

## Useful Commands

```bash
uv run nepali-tithi today
uv run nepali-tithi ad-to-bs 2026-06-13
uv run nepali-tithi bs-to-ad 2083-02-30
uv run nepali-tithi init-db
uv run nepali-tithi seed-sample-data
uv run nepali-tithi lookup-ad 2026-06-01
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```
