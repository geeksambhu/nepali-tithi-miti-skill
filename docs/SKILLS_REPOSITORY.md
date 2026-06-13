# Publishing And Using This In Skills Repositories

This repository supports both a full Python package layout and a portable agent-skill layout.

## Supported Layouts

### Full Package Repository

Use the full repo when you want:

- the `nepali-tithi` CLI
- SQLite cache support
- parsing and lookup code
- tests
- sample data
- future ingestion tooling
- a portable skill folder

### Portable Skill Repository

Use only this folder when a skills registry or agent wants a standalone skill package:

```text
skills/nepali-tithi-miti/
└── SKILL.md
```

The skill folder is intentionally small. It tells the agent when to use the skill, how to avoid guessing calendar fields, and how to call the companion CLI when installed.

## Install Into Another Skills Repository

Copy the folder under the target repository's `skills/` directory:

```bash
mkdir -p ~/my-skills-repo/skills
cp -R skills/nepali-tithi-miti ~/my-skills-repo/skills/
```

Expected result:

```text
my-skills-repo/
└── skills/
    └── nepali-tithi-miti/
        └── SKILL.md
```

## Codex

Install the portable folder into Codex's skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/nepali-tithi-miti "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then restart Codex or refresh skills if required by the client.

Suggested prompt:

```text
Use $nepali-tithi-miti to answer this Nepali date question. Use verified cached data and do not guess tithi.
```

## Claude

For Claude or Claude Code surfaces that support skills, keep the package shape as:

```text
nepali-tithi-miti/
└── SKILL.md
```

If the surface accepts uploads, zip the folder:

```bash
cd skills
zip -r nepali-tithi-miti.zip nepali-tithi-miti
```

If it reads local skills from disk, copy `skills/nepali-tithi-miti/` into that configured skills directory.

## GitHub Copilot

Copilot environments may use repository instructions instead of portable skills. Use one of these approaches:

- install `skills/nepali-tithi-miti/` directly if your Copilot surface supports agent skills
- otherwise, reference the skill from `.github/copilot-instructions.md`

Suggested `.github/copilot-instructions.md`:

```markdown
Use `skills/nepali-tithi-miti/SKILL.md` for Nepali Bikram Sambat, miti, tithi, panchang, festival, and AD/BS conversion requests.
Never guess tithi, nakshatra, yoga, karana, or festival dates. Use verified cached data or say the data is unavailable.
Prefer the `nepali-tithi` CLI when it is installed.
```

## OpenClaw, PicoClaw, OpenCode, And ClawHub-Style Registries

For OpenClaw, PicoClaw, OpenCode, and similar local-first agents, install this as a workspace or global skill:

```bash
mkdir -p ~/.openclaw/skills
cp -R skills/nepali-tithi-miti ~/.openclaw/skills/
```

If your agent has a different configured skills root, use that root instead. The expected structure is:

```text
<skills-root>/nepali-tithi-miti/SKILL.md
```

Recommended runtime requirements to list in a registry entry:

- Python 3.10+
- `uv`
- `uv sync --extra dev` install of this package for the `nepali-tithi` CLI
- local SQLite calendar cache for tithi, panchang, and festival data
- no secrets required
- no automatic network calls

## Marketplace Readiness Checklist

This repo includes a marketplace metadata entry:

```text
marketplace/nepali-tithi-miti.json
```

Before publishing online:

- Keep `SKILL.md` human-readable and auditable.
- Do not include hidden install scripts.
- Do not request credentials, browser cookies, wallet keys, SSH keys, or private files.
- Document every external dependency.
- Document that Hamro Patro-style ingestion is cache-first and only when allowed.
- Include tests and sample data when publishing the full repo.
- Avoid auto-running network calls.
- Keep generated caches out of the package unless they are intentionally licensed sample data.
- Use semantic version tags or release notes when changing skill behavior.

## Recommended Published Files

For a complete public repo, include:

```text
README.md
LICENSE
pyproject.toml
uv.lock
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
skills/nepali-tithi-miti/SKILL.md
skills/nepali-tithi-miti/agents/openai.yaml
marketplace/nepali-tithi-miti.json
docs/SKILLS_REPOSITORY.md
docs/nepalipatro-widget.html
src/nepali_tithi_miti/
tests/
data/sample_calendar_days.json
```

For a minimal skill registry submission, include:

```text
nepali-tithi-miti/
├── agents/
│   └── openai.yaml
└── SKILL.md
```

## Suggested Tags

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
agent-skill
```

## Suggested Marketplace Description

```text
Nepali Tithi Miti is a safe, cache-first Nepali calendar skill for Bikram Sambat dates, AD/BS conversion, tithi, panchang fields, Nepali festivals, and Nepal-time "today" lookups. It uses deterministic Python tooling and verified cached data rather than guessing.
```
