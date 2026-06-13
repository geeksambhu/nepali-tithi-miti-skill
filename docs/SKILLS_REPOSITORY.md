# Publishing / Using This in a Skills Repository

This repo supports two layouts:

## 1. Python package repo

Use the full repo when you want CLI, SQLite cache, tests, ingestion, and Python code.

## 2. Portable skills repository layout

Copy this folder into another skills repository:

```text
skills/nepali-tithi-miti/
└── SKILL.md
```

Example:

```bash
mkdir -p ~/my-skills-repo/skills
cp -R skills/nepali-tithi-miti ~/my-skills-repo/skills/
```

## ClawHub-style marketplace readiness

For a ClawHub-style skill marketplace, keep the skill transparent:

- include a clear `SKILL.md`
- avoid hidden install scripts
- avoid asking for credentials or private files
- document every external dependency
- document that Hamro Patro-style ingestion is cache-first and only when allowed
- include tests and sample data
- avoid auto-running network calls

## Suggested tags

```text
nepali
calendar
bikram-sambat
tithi
miti
panchang
festival
date-conversion
python
```

## Suggested marketplace description

Nepali Tithi Miti is a safe, cache-first Nepali calendar skill for Bikram Sambat dates, AD/BS conversion, tithi, panchang fields, Nepali festivals, and Nepal-time "today" lookups. It uses deterministic Python tooling and verified cached data rather than guessing.
