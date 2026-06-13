# Nepali Tithi Miti Claude Instructions

Use the portable skill at `skills/nepali-tithi-miti/SKILL.md` for Nepali date/calendar work.

Run local tooling with `uv`:

```bash
uv sync --extra dev
uv run nepali-tithi today
uv run pytest
```

For AD/BS conversion, prefer the local CLI, which uses the open-source `nepali-datetime` package:

```bash
uv run nepali-tithi ad-to-bs 2026-06-13
uv run nepali-tithi bs-to-ad 2083-02-30
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```

Never invent tithi, nakshatra, yoga, karana, panchang, or festival data. Use verified cached calendar/API records or say those fields are unavailable.
