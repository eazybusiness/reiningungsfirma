# Freelance Bid Workspace

A structured workspace for finding, bidding on, and winning freelance projects on [Freelancer.com](https://www.freelancer.com).

Each project bid lives in its own subfolder with its own bid text, planning document, and demo — shareable via GitHub link directly in the bid.

## How to Use

### Start every session

Run the `/init` workflow to restore context and pick up where you left off.

### Find new projects

Run `/find-projects` to search Freelancer.com via API, score projects against your profile, and get ranked recommendations.

### Create a bid

Run `/new-bid` to walk through a structured process:
1. Answer a few questions about the project
2. Get a 500–700 char winning bid text generated
3. Get a PLANNING.md + demo/strategic document created
4. Everything organized in its own subfolder with a git repo

## Workspace Structure

```
.planning/               ← GSD planning system (read at every session start)
  PROJECT.md             ← workspace identity + Nils's full context
  STATE.md               ← session continuity tracker
  REQUIREMENTS.md        ← scope, constraints, in/out of scope
  ROADMAP.md             ← phased milestones Q1–Q4 2026
  PROFILE.md             ← full skills, interests, positioning (used by workflows)

.windsurf/workflows/
  init.md                ← /init workflow
  find-projects.md       ← /find-projects workflow
  new-bid.md             ← /new-bid workflow

project-name/            ← one folder per bid
  BID.md                 ← bid text (paste into Freelancer.com)
  PLANNING.md            ← milestone plan + deliverables
  DEMO.md                ← proof asset / strategic document
  README.md              ← shareable via GitHub link

PLANNING.md              ← this workspace's planning overview
TASK.md                  ← active bids and pending items
.env                     ← FREELANCER_OAUTH_TOKEN (never committed)
```

## Profile

**Nils Peters** — Business Automation Advisor + Full Stack Developer
- 20+ years C-level experience (tech, e-commerce, industrial)
- Trilingual: German / English / Spanish
- Based in Bolivia, serving DACH clients remotely
- Website: [me.hiplus.de](https://me.hiplus.de)

## Related Projects

| Project | Purpose |
|---------|---------|
| `../freelance_api/` | Full automated pipeline with scoring + dashboard |
| `../freelance_brainstorming/` | Business strategy, positioning, LinkedIn |
| `../freelancer_scraper/` | Legacy scraper (pre-API) |

## Demo Projects

Demos linked in bids are deployed to GitHub Pages under [github.com/eazybusiness](https://github.com/eazybusiness).
