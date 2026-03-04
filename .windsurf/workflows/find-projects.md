---
description: Search Freelancer.com for new projects, score them against your profile, and recommend the best ones to bid on
---

## Find Projects Workflow

Use this workflow to discover new projects on Freelancer.com that match your skills and interests.

## Look out for

Be aware of the currency. use aproximate exchange rates to calculate the usd value.
Exclude offers from India or in INR.
Look for projects with less bids prefererably.
Distingues between hourly rates and fixed budgets.

### Step 1: Load profile context

Read `.planning/PROFILE.md` to load skills, interests, project preferences, and bid criteria.

### Step 2: Ask the user what to search for (optional)

**Default preferences (skip questions unless user wants to override):**
- Primary focus: German/DACH business projects (automation, ERP, CRM, process optimization)
- Secondary focus: AI-assisted IT projects (web apps, dashboards, data analysis)
- Min budget: €500 / $500 (only show €200+ if nothing else available or <1 hour work)
- Prefer: European clients over international
- Show: 10 valid projects

**Only ask if user wants to override defaults:**
Use workflow `/ask_user_questions` to ask:
- "Search for specific keywords or use default (German business + AI-assisted IT)?"
- "Different budget filter than €500+ minimum?"

### Step 3: Call the Freelancer.com API and filter results

Use the `FREELANCER_OAUTH_TOKEN` from `.env` to call the Freelancer.com API.

**Endpoint:** `GET https://www.freelancer.com/api/projects/0.1/projects/active`

**Important:** Request 50+ projects to ensure we get 10 valid ones after filtering.

Key parameters:
- `query`: Based on defaults or user override
- `min_budget`: 500 (USD)
- `full_description`: true
- `job_details`: true
- `limit`: 50 (to account for filtering)
- `sort_field`: time_updated

**Filter out these projects:**
1. **Deleted projects** — `deleted: true`
2. **Closed projects** — `frontend_project_status != "open"`
3. **Preferred freelancer only** — `upgrades.pf_only: true`
4. **Indian projects** — `location.country.code == "IN"` or currency is INR
5. **Already bid on** — check if user already placed a bid (requires checking bid history)
6. **Budget too low** — under €200/$200 (unless nothing else available)
7. **Non-existent/invalid** — missing critical fields (title, description, budget)

**Currency conversion (approximate):**
- EUR to USD: ×1.1
- GBP to USD: ×1.3
- AUD to USD: ×0.65
- INR to USD: ×0.012 (exclude these)

Run this command to search and filter:
```bash
curl -H "freelancer-oauth-v1: $(grep FREELANCER_OAUTH_TOKEN .env | cut -d= -f2)" \
  "https://www.freelancer.com/api/projects/0.1/projects/active?limit=50&full_description=true&job_details=true&query=German%20business%20OR%20Deutsch%20OR%20automation%20OR%20ERP%20OR%20CRM%20OR%20process%20optimization%20OR%20dashboard%20OR%20data%20analysis%20OR%20AI%20implementation&min_budget=500&sort_field=time_updated" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
projects = data.get('result', {}).get('projects', [])

# Filter valid projects
valid_projects = []
for p in projects:
    # Skip deleted
    if p.get('deleted', False):
        continue
    
    # Skip closed
    if p.get('frontend_project_status') != 'open':
        continue
    
    # Skip preferred freelancer only
    if p.get('upgrades', {}).get('pf_only', False):
        continue
    
    # Skip Indian projects
    country_code = p.get('location', {}).get('country', {}).get('code')
    if country_code == 'IN':
        continue
    
    # Skip if missing critical fields
    if not p.get('title') or not p.get('preview_description'):
        continue
    
    # Skip INR currency (currency_id 3 = INR)
    budget = p.get('budget', {})
    if budget and budget.get('currency_id') == 3:  # INR
        continue
    
    # Also check if budget values are too low (likely INR)
    if budget and budget.get('minimum', 0) < 200:
        continue
    
    valid_projects.append(p)
    
    # Stop when we have 10 valid projects
    if len(valid_projects) >= 10:
        break

print(f'Found {len(valid_projects)} valid projects (filtered from {len(projects)} total)')
for p in valid_projects:
    budget = p.get('budget', {})
    budget_min = budget.get('minimum', 0) if budget else 0
    budget_max = budget.get('maximum', 0) if budget else 0
    currency_id = budget.get('currency_id', 1) if budget else 1  # Default to USD (1)
    currency_map = {1: 'USD', 2: 'EUR', 3: 'INR', 4: 'GBP', 5: 'AUD', 6: 'CAD'}
    currency = currency_map.get(currency_id, 'USD')
    
    project_id = p.get('seo_url', f'projects/{p.get(\"id\", \"unknown\")}')
    url = f'https://www.freelancer.com/projects/{project_id}'
    
    print(f'\nTitle: {p[\"title\"]}')
    print(f'URL: {url}')
    print(f'Budget: {currency} {budget_min:.0f}-{budget_max:.0f}')
    print(f'Bids: {p.get(\"bid_stats\", {}).get(\"bid_count\", 0)}')
    print(f'Language: {p.get(\"language\", \"unknown\")}')
    print(f'Preview: {p.get(\"preview_description\", \"\")[:150]}...')
    print('---')
"
```

### Step 4: Score and rank the projects

For each valid project, score it on these dimensions (1–5 each):

| Dimension | What to check |
|-----------|--------------|
| **Skill match** | How well does it match PROFILE.md skills? Business automation/ERP/CRM = 5, AI-assisted IT = 4, general dev = 3 |
| **Budget** | Is the budget realistic? €1000+ = 5, €500-999 = 4, €200-499 = 2. Note if hourly or fixed. |
| **Competition** | How many bids already? <10 bids = 5, 10-20 = 4, 21-30 = 3, >30 = 1 |
| **Client quality** | Does client have reviews? Verified payment? Payment verified + reviews = 5 |
| **Language/Location** | German language = 5, European client = 4, English international = 3, other = 1 |
| **Win probability** | DACH client + good brief + can offer demo = 5, good brief = 3, unclear brief = 1 |

**Total score = sum of dimensions (max 30)**

**Priority order:**
1. German business projects (automation, ERP, CRM, process optimization)
2. European AI-assisted IT projects (dashboards, data analysis, web apps)
3. International high-value projects (only if €1000+)

### Step 5: Present recommendations

Show a ranked table:

```
# Project Recommendations

| Rank | Title | Budget | Bids | Score | Reason |
|------|-------|--------|------|-------|--------|
| 1 | ... | €500 | 7 | 24/30 | DACH client, exact skill match |
| 2 | ... | €800 | 12 | 21/30 | German language, good brief |
| 3 | ... | €300 | 4 | 19/30 | Low competition, quick demo possible |
```

For each top project, include:
- Project title + URL
- Budget range
- Number of existing bids
- Score breakdown
- **Why this is a good match** (1–2 sentences)
- **Suggested angle** for the bid

### Step 6: Ask the user what to do next

Ask the user:
- Which projects to bid on now (run `/new-bid` for each)
- Which to skip (and why — for future learning)
- Whether to run another search with different keywords

### Step 7: Update TASK.md and STATE.md

Add selected projects to `TASK.md` as pending bids.
Update `.planning/STATE.md` with today's date and what was found.
