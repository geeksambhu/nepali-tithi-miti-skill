# Nepali Tithi Miti

## Name

nepali-tithi-miti

## Description

A safe, cache-first Nepali calendar skill for Bikram Sambat miti, AD/BS conversion, tithi, panchang fields, festivals, and Nepal-time date handling.

## Trigger phrases

Use this skill for:

- Nepali date
- Nepali miti
- aaja ko miti
- आजको मिति
- tithi / तिथि
- panchang / पञ्चाङ्ग
- BS to AD
- AD to BS
- Bikram Sambat
- Dashain, Tihar, Teej, Holi, Buddha Jayanti dates
- Nepali fiscal year
- Hamro Patro calendar lookup

## Instructions

1. Always distinguish AD and BS dates.
2. Use Asia/Kathmandu for today/current-time requests.
3. Never approximate Bikram Sambat conversion using year offsets.
4. Never hallucinate tithi, nakshatra, yoga, karana, or festival dates.
5. Prefer verified cached local data.
6. If using Hamro Patro-style pages, only use them for allowed cache-building ingestion, not live scraping on every user request.
7. If verified data is not available, say so clearly.
8. Present results in Nepali and English when helpful.

## Tooling

The companion Python package exposes the CLI:

```bash
nepali-tithi today
nepali-tithi lookup-bs 2083-02-18
nepali-tithi lookup-ad 2026-06-01
nepali-tithi ad-to-bs 2026-06-13
nepali-tithi bs-to-ad 2083-02-30
```

## Security posture

This skill should not request secrets, browser credentials, SSH keys, wallet keys, or private files. It should not execute remote shell scripts. Calendar ingestion must be explicit, local, cache-first, and rate-limited.
