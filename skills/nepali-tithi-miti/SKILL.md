---
name: nepali-tithi-miti
description: Safe, cache-first Nepali calendar support for Bikram Sambat miti, AD/BS conversion, Nepal-time "today" requests, tithi, panchang fields, festivals, and Hamro Patro-style calendar lookup. Use when the user asks about Nepali dates, miti, tithi, panchang, Bikram Sambat, Dashain/Tihar/Teej/Holi/Buddha Jayanti dates, Nepali fiscal years, BS/AD conversion, or verified Nepali calendar data.
---

# Nepali Tithi Miti

## Use For

- Nepali date
- Nepali miti
- aaja ko miti
- aaja ko tithi
- aajako tithi
- आजको मिति
- आजको तिथि
- Nepali calendar lookup
- tithi / तिथि
- panchang / पञ्चाङ्ग
- BS to AD
- AD to BS
- Bikram Sambat
- Dashain, Tihar, Teej, Holi, Buddha Jayanti dates
- Nepali fiscal year
- Hamro Patro calendar lookup

## Rules

1. Always distinguish AD and BS dates.
2. Use Asia/Kathmandu for today/current-time requests.
3. Never approximate Bikram Sambat conversion using year offsets.
4. Never hallucinate tithi, nakshatra, yoga, karana, or festival dates.
5. Prefer verified cached local data.
6. If using Hamro Patro-style pages, only use them for allowed cache-building ingestion, not live scraping on every user request.
7. If verified data is not available, say so clearly.
8. Present results in Nepali and English when helpful.

## Tooling

When the companion Python package is installed with `uv sync --extra dev`, use the deterministic CLI before answering:

```bash
uv run nepali-tithi today
uv run nepali-tithi lookup-bs 2083-02-18
uv run nepali-tithi lookup-ad 2026-06-01
uv run nepali-tithi ad-to-bs 2026-06-13
uv run nepali-tithi bs-to-ad 2083-02-30
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```

If the CLI or verified data is unavailable, explain what is missing and do not invent calendar fields.

For live user-requested tithi/miti lookup, run source extraction first:

```bash
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date YYYY-MM-DD --source all --cache
```

This tries Hamro Patro first, then NepaliPatro and NepalCalendar/PrabhuPatro fallbacks where they can provide useful data. Use `uv run nepali-tithi today` only as an offline BS date fallback when scraping is unavailable.

Default SQLite cache:

```text
~/.nepali_tithi_miti/calendar.sqlite3
```

Override with:

```bash
export NEPALI_TITHI_MITI_DB=/path/to/calendar.sqlite3
```

## Output Pattern

Prefer a compact bilingual answer when data is available:

```text
नेपाली मिति: २०८३ जेठ १८, सोमबार
English date: 2026-06-01
तिथि: अधिक जेठ कृष्ण प्रतिपदा
पर्व/बिदा: -
Source: cached verified calendar data
Confidence: medium
```

## Security Posture

This skill should not request secrets, browser credentials, SSH keys, wallet keys, or private files. It should not execute remote shell scripts. Calendar ingestion must be explicit, local, cache-first, and rate-limited.
