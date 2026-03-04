# PLANNING — Freelance Bid Workspace

> This workspace is the engine for finding, bidding on, and winning freelance projects on Freelancer.com.
> Each project lives in its own subfolder with its own bid, demo, and planning documents.

## Start Here Every Session

1. Read `.planning/STATE.md` — what happened last session, what's next
2. Read `.planning/PROJECT.md` — who we are and what this produces
3. Check `TASK.md` — what's active right now
4. Run `/find-projects` if you have bid credits to use

## Planning Structure

```
.planning/
  PROJECT.md        ← workspace identity, who is Nils, what this produces
  STATE.md          ← session continuity tracker (update before leaving)
  REQUIREMENTS.md   ← scope, constraints, what's in/out
  ROADMAP.md        ← phased milestones (Q1–Q4 2026)
  PROFILE.md        ← full skills, interests, positioning (used by workflows)
```

## Workflows

| Slash Command | Purpose |
|--------------|---------|
| `/init` | Start a new session: reads planning files, summarizes state |
| `/find-projects` | Search Freelancer.com API, score projects, recommend top picks |
| `/new-bid` | Ask questions → generate 500–700 char bid + demo + subfolder + git |

## Project Structure

Every bid lives in its own subfolder:
```
project-name/
  BID.md          ← 500–700 char bid text (paste into Freelancer.com)
  PLANNING.md     ← milestone plan, scope, deliverables
  DEMO.md         ← demo analysis / strategic document / proof asset
  README.md       ← shareable via GitHub link
```

## Key Rules

- **No loose files at root** — every bid in its own folder
- **Bid text: 500–700 chars** — tight, winning, client-pain-first
- **Always include a demo or link** — differentiates from 100+ generic bids
- **Match project language** — German for DACH, English for international
- **Never bid below €200/$200** — not worth the overhead
- **`.env` never in git** — `FREELANCER_OAUTH_TOKEN` stays local

## Architecture Decisions

- **Freelancer.com API** — used via `FREELANCER_OAUTH_TOKEN` in `.env`
- **Profile reference:** `.planning/PROFILE.md` — skills, interests, positioning
- **LinkedIn texts:** `../freelance_brainstorming/.planning/linkedin_copy_paste.md`
- **Advanced pipeline (cron + dashboard):** `../freelance_api/` project

## Related Projects

| Project | Path | Purpose |
|---------|------|---------|
| Freelancer AI Dashboard | `../freelance_api/` | Full automated pipeline with scoring + email |
| Freelance Brainstorming | `../freelance_brainstorming/` | Business strategy, LinkedIn, positioning |
| Freelancer Scraper | `../freelancer_scraper/` | Legacy scraper (pre-API) |
