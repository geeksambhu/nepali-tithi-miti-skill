# Nepali Tithi Miti Skill

## Description

Use this skill for Nepali Bikram Sambat calendar work: AD/BS conversion, today's Nepali date, tithi/miti lookup, Nepali festival lookup, and panchang-style calendar fields when verified cached data is available.

## When to use

Use this skill when the user asks about:

- Nepali date, miti, मिति
- Bikram Sambat, BS, विक्रम संवत्
- AD to BS conversion
- BS to AD conversion
- tithi, तिथि
- panchang, पञ्चाङ्ग
- nakshatra, नक्षत्र
- yoga, योग
- karana, करण
- Nepali festivals such as Dashain, Tihar, Teej, Holi, Buddha Jayanti
- Nepali fiscal year
- age calculation from BS date

## Core rules

1. Do not guess BS/AD conversion manually.
2. Do not calculate tithi from simple rules.
3. Use a deterministic conversion library or verified cached calendar dataset.
4. Use `Asia/Kathmandu` for "today", "now", "aaja", and "आज".
5. If panchang/tithi data is missing, say unavailable instead of inventing.
6. Festival dates must come from a verified dataset.
7. Always label AD and BS dates clearly.
8. Support English, Nepali Devanagari, and Romanized Nepali queries.
9. For Hamro Patro or similar sources, use cache-building ingestion only when allowed. Never scrape aggressively or live per user request.

## Preferred output

```text
नेपाली मिति: २०८३ जेठ १८, सोमबार
English date: 2026-06-01
तिथि: अधिक जेठ कृष्ण प्रतिपदा
पञ्चाङ्ग: Pratipada
पर्व/बिदा: —
Source: cached verified calendar data
Confidence: medium
```
