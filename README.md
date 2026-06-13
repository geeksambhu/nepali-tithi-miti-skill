# Nepali Tithi Miti Skill

Python package and CLI for Nepali Bikram Sambat date/calendar workflows:

- AD to BS conversion
- BS to AD conversion
- today's Nepali date using `Asia/Kathmandu`
- tithi/miti lookup from a local SQLite cache
- festival/holiday lookup from cached calendar records
- safe cache-first ingestion design for Hamro Patro-style calendar pages
- portable skill files under `skills/nepali-tithi-miti/`

> Important: exact tithi, panchang, festival, nakshatra, yoga, and karana values should come from verified calendar data. The code intentionally does not let an LLM guess these values.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## CLI examples

```bash
nepali-tithi today
nepali-tithi ad-to-bs 2026-06-13
nepali-tithi bs-to-ad 2083-02-30
nepali-tithi lookup-bs 2083-02-18
nepali-tithi lookup-ad 2026-06-01
nepali-tithi init-db
nepali-tithi seed-sample-data
```

Default SQLite DB:

```text
~/.nepali_tithi_miti/calendar.sqlite3
```

Override with:

```bash
export NEPALI_TITHI_MITI_DB=/path/to/calendar.sqlite3
```

## Skills repository compatibility

This repo includes a portable skill directory:

```text
skills/nepali-tithi-miti/SKILL.md
```

You can copy that folder into a separate Claude/OpenCode/OpenClaw/ClawHub-style skills repository. See `docs/SKILLS_REPOSITORY.md`.

## Data strategy

Recommended priority:

1. Official/permissioned Nepali calendar or panchang API
2. Open licensed Nepali calendar dataset
3. Your own verified local dataset
4. Cache-building ingestion from public calendar pages only when allowed

Do not scrape aggressively. Do not scrape live per user request. Store source URL, fetched timestamp, and confidence.
