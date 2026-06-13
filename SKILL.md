---
name: nepali-tithi-miti
description: Safe, cache-first Nepali calendar support for Bikram Sambat miti, AD/BS conversion, Nepal-time "today" requests, tithi, panchang fields, festivals, and Hamro Patro-style calendar lookup. Use when the user asks about Nepali dates, miti, tithi, panchang, Bikram Sambat, Dashain/Tihar/Teej/Holi/Buddha Jayanti dates, Nepali fiscal years, BS/AD conversion, or verified Nepali calendar data.
---

# Nepali Tithi Miti Skill

Use this skill for Nepali Bikram Sambat calendar work: AD/BS conversion, today's Nepali date, tithi/miti lookup, Nepali festival lookup, and panchang-style calendar fields when verified cached data is available.

## Rules

1. Do not guess BS/AD conversion manually.
2. Do not calculate tithi from simple rules.
3. Use a deterministic conversion library or verified cached calendar dataset.
4. Use `Asia/Kathmandu` for "today", "now", "aaja", and "आज".
5. If panchang/tithi data is missing, say unavailable instead of inventing.
6. Festival dates must come from a verified dataset.
7. Always label AD and BS dates clearly.
8. Support English, Nepali Devanagari, and Romanized Nepali queries.
9. For Hamro Patro or similar sources, use cache-building ingestion only when allowed. Never scrape aggressively or live per user request.

## Tooling

When this repository is installed with `uv sync --extra dev`, prefer the local CLI:

```bash
uv run nepali-tithi today
uv run nepali-tithi ad-to-bs 2026-06-13
uv run nepali-tithi bs-to-ad 2083-02-30
uv run nepali-tithi lookup-bs 2083-02-18
uv run nepali-tithi lookup-ad 2026-06-01
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```

Default SQLite cache:

```text
~/.nepali_tithi_miti/calendar.sqlite3
```

Override with:

```bash
export NEPALI_TITHI_MITI_DB=/path/to/calendar.sqlite3
```

For live user-requested tithi/miti lookup, use `uv run nepali-tithi scrape-today --source all --cache` or `uv run nepali-tithi scrape-date YYYY-MM-DD --source all --cache`. This first tries Hamro Patro, then falls back to NepaliPatro and NepalCalendar/PrabhuPatro where usable.

## Preferred Output

```text
नेपाली मिति: २०८३ जेठ १८, सोमबार
English date: 2026-06-01
तिथि: अधिक जेठ कृष्ण प्रतिपदा
पञ्चाङ्ग: Pratipada
पर्व/बिदा: -
Source: cached verified calendar data
Confidence: medium
```

## Portable Package

The registry-ready copy is:

```text
skills/nepali-tithi-miti/SKILL.md
```

Marketplace metadata is:

```text
marketplace/nepali-tithi-miti.json
```
