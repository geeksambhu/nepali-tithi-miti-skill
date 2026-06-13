# Nepali Tithi Miti Skill

Python package, CLI, and portable agent skill for Nepali Bikram Sambat calendar workflows.

This project is designed for two use cases:

- deterministic local tooling for Nepali date/calendar lookups
- a portable `SKILL.md` folder that coding agents can load as a reusable skill
- a Codex-style plugin manifest for marketplace installation

The skill covers:

- AD to BS conversion
- BS to AD conversion
- today's Nepali date using `Asia/Kathmandu`
- tithi/miti lookup from a local SQLite cache
- festival/holiday lookup from cached calendar records
- safe cache-first ingestion design for Hamro Patro-style calendar pages
- portable skill files under `skills/nepali-tithi-miti/`

> Important: exact tithi, panchang, festival, nakshatra, yoga, and karana values must come from verified calendar data. The code and skill intentionally tell agents not to guess these values.

## Install The Python Tool

Use the full repository when you want the CLI, SQLite cache, sample data, tests, and Python package.

```bash
uv sync --extra dev
```

Run the tests:

```bash
uv run pytest
```

## CLI Examples

```bash
uv run nepali-tithi today
uv run nepali-tithi ad-to-bs 2026-06-13
uv run nepali-tithi bs-to-ad 2083-02-30
uv run nepali-tithi lookup-bs 2083-02-18
uv run nepali-tithi lookup-ad 2026-06-01
uv run nepali-tithi init-db
uv run nepali-tithi seed-sample-data
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```

## NepaliPatro Widget Preview

Open this file in a browser to render the live NepaliPatro day widget:

```text
docs/nepalipatro-widget.html
```

It embeds:

```html
<div id="np_widget_wiz1" widget="day" style="width: 300px;"></div>
<script async src="https://nepalipatro.com.np/np-widgets/nepalipatro.js" id="wiz1"></script>
```

Default SQLite DB:

```text
~/.nepali_tithi_miti/calendar.sqlite3
```

Override with:

```bash
export NEPALI_TITHI_MITI_DB=/path/to/calendar.sqlite3
```

## Install As An Agent Skill

The portable skill lives here:

```text
skills/nepali-tithi-miti/
└── SKILL.md
```

Copy the whole folder into any agent skills directory or skills repository that supports the common `SKILL.md` folder format:

```bash
mkdir -p ~/my-agent-skills/skills
cp -R skills/nepali-tithi-miti ~/my-agent-skills/skills/
```

After installation, ask the agent questions such as:

```text
Use the Nepali Tithi Miti skill to convert 2026-06-13 AD to BS.
Use nepali-tithi-miti to look up aaja ko miti.
Use the skill to find the tithi for BS 2083-02-18 from verified cached data.
```

For best results, run `uv sync --extra dev` in the same workspace or environment where the agent runs, so the skill can call `uv run nepali-tithi`.

## Codex

For Codex-style skill loading, copy the portable skill folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nepali-tithi-miti "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then restart Codex or refresh its skill index if your client requires it.

Use prompts like:

```text
Use $nepali-tithi-miti to answer today's Nepali miti in Nepal time.
Use the Nepali Tithi Miti skill and do not guess tithi if cached data is missing.
```

## Claude

For Claude or Claude Code environments that support skills, package or copy the folder exactly as:

```text
nepali-tithi-miti/
└── SKILL.md
```

If the Claude surface expects uploads, zip the folder itself:

```bash
cd skills
zip -r nepali-tithi-miti.zip nepali-tithi-miti
```

If the Claude surface reads local skills from a configured directory, copy `skills/nepali-tithi-miti/` into that directory. Keep the folder name and `SKILL.md` filename unchanged.

## GitHub Copilot

GitHub Copilot commonly uses repository instructions rather than portable skill folders. Use this repo in either of these ways:

1. If your Copilot environment supports agent skills, install `skills/nepali-tithi-miti/` as a normal `SKILL.md` skill folder.
2. If it does not, reference the skill from repository instructions such as `.github/copilot-instructions.md`.

Example `.github/copilot-instructions.md`:

```markdown
Use `skills/nepali-tithi-miti/SKILL.md` for Nepali Bikram Sambat, miti, tithi, panchang, festival, and AD/BS conversion requests.
Never guess tithi, nakshatra, yoga, karana, or festival dates. Use verified cached data or say the data is unavailable.
Prefer the `nepali-tithi` CLI when it is installed.
```

## OpenClaw, PicoClaw, OpenCode, And Similar Agents

For OpenClaw, PicoClaw, OpenCode, ClawHub-style registries, and similar local-first agents, install this as a workspace or global skill:

```bash
mkdir -p ~/.openclaw/skills
cp -R skills/nepali-tithi-miti ~/.openclaw/skills/
```

If your agent uses a different directory, copy the same folder into that configured skills path. The important structure is:

```text
<skills-root>/nepali-tithi-miti/SKILL.md
```

Recommended agent prompt:

```text
Use nepali-tithi-miti for Nepali calendar work. Use `uv run nepali-tithi scrape-today --source all --cache` when the user asks for live today's miti/tithi, then use the local cache for follow-up answers.
```

## Publish In Online Skill Repositories

This repo now includes a reusable marketplace listing:

```text
marketplace/nepali-tithi-miti.json
```

It also includes a Codex-style plugin manifest:

```text
plugins/nepali-tithi-miti/.codex-plugin/plugin.json
.agents/plugins/marketplace.json
```

When publishing to a public skills repository, include:

- `skills/nepali-tithi-miti/SKILL.md`
- `skills/nepali-tithi-miti/agents/openai.yaml`
- `plugins/nepali-tithi-miti/.codex-plugin/plugin.json`
- `plugins/nepali-tithi-miti/skills/nepali-tithi-miti/`
- `.agents/plugins/marketplace.json`
- `marketplace/nepali-tithi-miti.json`
- `LICENSE`
- this `README.md`
- `docs/SKILLS_REPOSITORY.md`
- `docs/nepalipatro-widget.html`
- `pyproject.toml`
- `uv.lock`
- `src/nepali_tithi_miti/`
- `tests/`
- `data/sample_calendar_days.json`

Recommended repository layout:

```text
nepali-tithi-miti-skill/
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── nepali-tithi-miti/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── nepali-tithi-miti/
├── skills/
│   └── nepali-tithi-miti/
│       ├── agents/
│       │   └── openai.yaml
│       └── SKILL.md
├── marketplace/
│   └── nepali-tithi-miti.json
├── src/
├── tests/
├── data/
└── docs/
```

For marketplace validators, submit the plugin path as `plugins/nepali-tithi-miti`, not `.`.

After pushing, enable repository security settings on GitHub:

- Settings > Code security > Code scanning: enable CodeQL default setup or use this repo's CodeQL workflow.
- Settings > Code security > Dependabot: enable Dependabot alerts.
- Settings > Rules > Rulesets: add a tag ruleset for `v*` tags to keep releases immutable.

Suggested tags:

```text
nepali, calendar, bikram-sambat, tithi, miti, panchang, festival, date-conversion, python, skill
```

Suggested marketplace description:

```text
Nepali Tithi Miti is a safe, cache-first Nepali calendar skill for Bikram Sambat dates, AD/BS conversion, tithi, panchang fields, Nepali festivals, and Nepal-time "today" lookups. It uses deterministic Python tooling and verified cached data rather than guessing.
```

## Data Strategy

Recommended priority:

1. `nepali-datetime` for deterministic AD/BS date conversion
2. Official or permissioned Nepali calendar or panchang API
3. Hamro Patro or Nepali Patro API/cache data when you have permission and stable access
4. Open licensed Nepali calendar dataset
5. Your own verified local dataset
6. Cache-building ingestion from public calendar pages only when allowed

Use scraping only for explicit user-requested lookup or cache refresh:

```bash
uv run nepali-tithi scrape-today --source hamropatro --cache
uv run nepali-tithi scrape-today --source nepalicalendar --cache
uv run nepali-tithi scrape-today --source all --cache
uv run nepali-tithi scrape-date 2026-06-13 --source all --cache
```

Do not scrape aggressively. Store source URL, fetched timestamp, and confidence.
