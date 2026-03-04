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

**Use browser-style filters to avoid INR projects:**
- Skills: 156,594,245,149,17,3,9,500,2490,1829,13,22,31,37,95,180,335,502,518,619,620,930,1000,1094,1679,2719
- Languages: en, de, es
- Countries: BE, FI, NO, SE, DK, NL, ES, CH, AT, DE, US, GB, CA, AU, FR

**Correct API parameters from official SDK:**
- `project_types[]`: fixed, hourly
- `countries[]`: BE, FI, NO, SE, DK, NL, ES, CH, AT, DE, US, GB, CA, AU, FR
- `languages[]`: en, de, es
- `jobs[]`: skill IDs (156,594,245,149,17,3,9,500,2490,1829,13,22,31,37,95,180,335,502,518,619,620,930,1000,1094,1679,2719)
- `min_avg_price`: minimum average price for fixed projects
- `min_avg_hourly_rate`: minimum hourly rate
- `sort_field`: time_updated

Run this command to search and filter:
```bash
curl -H "freelancer-oauth-v1: $(grep FREELANCER_OAUTH_TOKEN .env | cut -d= -f2)" \
  "https://www.freelancer.com/api/projects/0.1/projects/active?limit=50&full_description=true&job_details=true&project_types[]=fixed&project_types[]=hourly&countries[]=BE&countries[]=FI&countries[]=NO&countries[]=SE&countries[]=DK&countries[]=NL&countries[]=ES&countries[]=CH&countries[]=AT&countries[]=DE&countries[]=US&countries[]=GB&countries[]=CA&countries[]=AU&countries[]=FR&languages[]=en&languages[]=de&languages[]=es&jobs[]=156&jobs[]=594&jobs[]=245&jobs[]=149&jobs[]=17&jobs[]=3&jobs[]=9&jobs[]=500&jobs[]=2490&jobs[]=1829&jobs[]=13&jobs[]=22&jobs[]=31&jobs[]=37&jobs[]=95&jobs[]=180&jobs[]=335&jobs[]=502&jobs[]=518&jobs[]=619&jobs[]=620&jobs[]=930&jobs[]=1000&jobs[]=1094&jobs[]=1679&jobs[]=2719&min_avg_price=500&min_avg_hourly_rate=20&sort_field=time_updated" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
projects = data.get('result', {}).get('projects', [])

print(f'Total projects from API: {len(projects)}')

# Filter valid projects
valid_projects = []
for p in projects:
    # Skip deleted/closed
    if p.get('deleted', False) or p.get('frontend_project_status') != 'open':
        continue
    if p.get('upgrades', {}).get('pf_only', False):
        continue
    
    # Must have title and description
    if not p.get('title') or not p.get('preview_description'):
        continue
    
    # Skip medical/design
    title_lower = p.get('title', '').lower()
    desc_lower = p.get('preview_description', '').lower()
    if any(kw in title_lower or kw in desc_lower for kw in ['medical', 'hospital', 'healthcare', 'clinical', 'patient', 'logo', 'graphic', 'illustration', 'vector', 'cartoon']):
        continue
    
    # Budget checks
    budget = p.get('budget', {})
    project_type = p.get('type', 'fixed')
    budget_min = budget.get('minimum', 0) if budget else 0
    
    # Skip suspiciously low budgets (likely INR)
    if project_type == 'fixed' and budget_min < 500:
        continue
    if project_type == 'hourly' and budget_min < 20:
        continue
    
    # Skip if currency is INR
    if budget and budget.get('currency_id') == 3:
        continue
    
    # Only include if country is actually set (not None)
    country_code = p.get('location', {}).get('country', {}).get('code')
    if not country_code:
        continue
    
    # Only first-world countries
    if country_code not in ['US', 'GB', 'CA', 'AU', 'DE', 'AT', 'CH', 'FR', 'NL', 'BE', 'SE', 'NO', 'DK', 'FI', 'ES']:
        continue
    
    valid_projects.append(p)

print(f'Valid projects after filtering: {len(valid_projects)}')

# If no valid projects with strict country filter, relax it
if len(valid_projects) == 0:
    print('No projects with valid country codes found. Relaxed filtering...')
    valid_projects = []
    for p in projects:
        # Basic filters only
        if p.get('deleted', False) or p.get('frontend_project_status') != 'open':
            continue
        if p.get('upgrades', {}).get('pf_only', False):
            continue
        if not p.get('title') or not p.get('preview_description'):
            continue
        
        # Skip medical/design
        title_lower = p.get('title', '').lower()
        desc_lower = p.get('preview_description', '').lower()
        if any(kw in title_lower or kw in desc_lower for kw in ['medical', 'hospital', 'healthcare', 'clinical', 'patient', 'logo', 'graphic', 'illustration', 'vector', 'cartoon']):
            continue
        
        # Budget checks (higher threshold to avoid INR)
        budget = p.get('budget', {})
        project_type = p.get('type', 'fixed')
        budget_min = budget.get('minimum', 0) if budget else 0
        
        if project_type == 'fixed' and budget_min < 1000:  # Higher threshold
            continue
        if project_type == 'hourly' and budget_min < 30:
            continue
        
        valid_projects.append(p)

# Show top 10
for i, p in enumerate(valid_projects[:10], 1):
    budget = p.get('budget', {})
    budget_min = budget.get('minimum', 0) if budget else 0
    budget_max = budget.get('maximum', 0) if budget else 0
    currency_id = budget.get('currency_id', 1) if budget else 1
    currency_map = {1: 'USD', 2: 'EUR', 3: 'INR', 4: 'GBP', 5: 'AUD', 6: 'CAD'}
    currency = currency_map.get(currency_id, 'USD')
    
    project_type = p.get('type', 'fixed')
    bid_count = p.get('bid_stats', {}).get('bid_count', 0)
    country_code = p.get('location', {}).get('country', {}).get('code', '?')
    language = p.get('language', 'unknown')
    
    project_id = p.get('seo_url', f\"projects/{p.get('id', 'unknown')}\")
    url = f'https://www.freelancer.com/projects/{project_id}'
    
    print(f'{i}. {p[\"title\"]}')
    print(f'   Type: {project_type.upper()} | Country: {country_code} | Language: {language}')
    if project_type == 'hourly':
        print(f'   Rate: {currency} {budget_min}-{budget_max}/hour | Bids: {bid_count}')
    else:
        print(f'   Budget: {currency} {budget_min}-{budget_max} | Bids: {bid_count}')
    print(f'   URL: {url}')
    print(f'   Preview: {p.get(\"preview_description\", \"\")[:120]}...')
    print()
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
