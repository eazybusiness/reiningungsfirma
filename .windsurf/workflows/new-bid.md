---
description: Create a winning bid for a specific project - asks questions, generates 500-700 char bid text, creates demo/strategic files, and sets up own subfolder with git repo
---

## New Bid Workflow

Use this to create a complete, winning bid package for a specific Freelancer.com project.

### Step 1: Load profile context

Read `.planning/PROFILE.md` for skills, positioning, and bid style rules.

### Step 2: Ask the user about the project

Use `ask_user_question` for each question below. Do NOT skip questions — each answer shapes the bid.

**Question 1 — Project type:**
- Web / app development (full-stack, frontend, backend)
- Business automation / AI / process consulting
- ERP / CRM implementation (Odoo, custom)
- Copywriting / content / ghostwriting
- Data analysis / scraping / dashboards
- Marketing (Meta Ads, Google Ads, SEO)
- Other / mixed

**Question 2 — Project language:**
- German (DACH market)
- English (international)
- Spanish

**Question 3 — Project scope and budget (ask user to paste or describe):**
Ask the user to paste the project description or provide a short summary. Also ask for the budget range if known.

**Question 4 — Client signals (ask user to describe):**
- Does the client have reviews / verified payment?
- How many bids are already placed?
- Any special requirements or red flags in the description?

**Question 5 — Demo / differentiation angle:**
- Live demo (deployable web app or page)
- Strategic document / analysis plan (PLANNING.md or DEMO.md)
- Data sample / scraper output / analysis snippet
- Code snippet / proof of concept
- No demo needed (bid text only)

**Question 6 — Bid tone:**
- Advisory / consulting (lead with business value)
- Technical expert (lead with specific tech skills)
- Value-for-money (competitive, efficient delivery)
- Partnership (long-term collaboration angle)

### Step 3: Generate the project folder name

Create a kebab-case folder name from the project topic, e.g.:
- `odoo-inventory-migration`
- `shopify-checkout-customization`
- `python-data-analysis-dashboard`
- `german-copywriting-tech-startup`

### Step 4: Create the subfolder and initialize git

```bash
mkdir -p FOLDER_NAME
cd FOLDER_NAME
git init
```

### Step 5: Generate the bid text (BID.md)

Write a BID.md with:
- **Bid text** (500–700 characters, in the project's language)
  - First line: hook that mirrors the client's pain
  - Middle: 1–2 specific credentials or proof points from PROFILE.md
  - End: clear next step + optional demo link placeholder
- **Bid notes** (internal, not pasted into Freelancer.com):
  - Why this project was selected
  - Competitor analysis (if known)
  - Follow-up message template (for after bid is accepted)
  - Questions to ask after project is awarded

**Bid text rules:**
- 500–700 characters TOTAL (count including spaces)
- No generic opener ("I read your project and...")
- Use "Sie" for German formal, "you" for English
- Mention ONE specific technical/business credential
- Include link to demo/planning doc if created: `Details: github.com/eazybusiness/FOLDER_NAME`
- End with a clear, low-friction call to action

### Step 6: Generate the PLANNING.md

Create a `PLANNING.md` in the subfolder with:
- Project overview (what the client wants)
- Proposed approach (how you would solve it)
- Milestone plan (3–5 milestones with deliverables and timeframes)
- Tech stack / tools proposed
- Pricing estimate
- What makes this bid unique

### Step 7: Generate the demo or strategic document

Based on the user's answer in Question 5:

**If live demo:**
- Create a minimal but functional prototype (HTML/React/Python)
- Deploy to GitHub Pages if possible
- Note: keep it clean and linkable

**If strategic document (DEMO.md):**
- Write a structured analysis or plan that proves you understand the project deeply
- Include: problem definition, proposed solution, implementation steps, expected outcomes
- Show domain knowledge (use real tools, frameworks, data patterns)

**If code snippet / proof:**
- Write a relevant code sample (Python function, React component, SQL query, etc.)
- Include in a `demo/` subfolder with a README

**If no demo:**
- Skip this step

### Step 8: Generate README.md

Create a `README.md` that is clean and shareable via GitHub:
- Project title
- What this folder contains
- Bid text (so client can read it)
- Planning document summary
- How to view the demo (if any)

### Step 9: First git commit

```bash
cd FOLDER_NAME
git add .
git commit -m "Initial bid package: BID, PLANNING, DEMO"
```

### Step 10: Update workspace TASK.md

Add a new entry in `TASK.md`:
```
### project-name
**Added:** YYYY-MM-DD
**Status:** Bid submitted / Pending response
- [ ] Submit bid on Freelancer.com
- [ ] Follow up if no response in 48h
- [ ] [If won] Create delivery folder outside this workspace
```

### Step 11: Update .planning/STATE.md

Note the new bid, the project type, and the date in `.planning/STATE.md`.

### Step 12: Final checklist before submitting

Present the user with a checklist:
- [ ] Bid text is exactly 500–700 characters (count it)
- [ ] Bid mentions a specific, relevant credential
- [ ] Demo/document link is included (or not needed)
- [ ] Tone matches the client's language and register
- [ ] No typos (especially in German formal)
- [ ] PLANNING.md is clean and linkable
- [ ] Subfolder has been git committed
