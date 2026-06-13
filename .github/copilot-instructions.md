# Copilot Instructions

Use `skills/nepali-tithi-miti/SKILL.md` for Nepali Bikram Sambat, miti, tithi, panchang, festival, and AD/BS conversion requests.

Install and run this project with `uv`:

```bash
uv sync --extra dev
uv run nepali-tithi today
uv run pytest
```

Rules:

- Use the local `nepali-tithi` CLI for AD/BS conversion.
- The CLI uses the open-source `nepali-datetime` package for deterministic conversion.
- Do not guess tithi, nakshatra, yoga, karana, panchang, or festival dates.
- Use verified cached calendar/API data for panchang fields.
- For explicit live today lookup, use `uv run nepali-tithi scrape-today --source all --cache`.
- For a specific AD date, use `uv run nepali-tithi scrape-date YYYY-MM-DD --source all --cache`.
- Use `Asia/Kathmandu` for today/current-time requests.
- If verified cache/API data is missing, return the converted BS date and clearly mark tithi/panchang unavailable.
