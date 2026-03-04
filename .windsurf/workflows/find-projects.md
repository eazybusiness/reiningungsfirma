---
description: Search Freelancer.com for new projects, score them against your profile, and recommend the best ones to bid on
---

## Find Projects Workflow

Use this workflow to discover new projects on Freelancer.com that match your skills and interests.

### Step 1: Load profile context

Read `.planning/PROFILE.md` to load skills, interests, project preferences, and bid criteria.

### Step 2: Ask the user what to search for

Ask the user these questions (use ask_user_question for each):

**Question 1 — Search focus:**
- DACH/German market (German-language projects)
- Full-stack / web development (international)
- Business automation / AI / process consulting
- Copywriting / ghostwriting / content
- Let me specify keywords manually

**Question 2 — Budget filter:**
- Any budget (show all)
- Min €200 / $200 only
- Min €500 / $500 only
- Min €1,000 / $1,000 only

**Question 3 — How many projects to review:**
- Show top 5 (quick scan)
- Show top 10 (thorough review)
- Show top 20 (full batch)

### Step 3: Call the Freelancer.com API

Use the `FREELANCER_OAUTH_TOKEN` from `.env` to call the Freelancer.com API.

**Endpoint:** `GET https://www.freelancer.com/api/projects/0.1/projects/active`

Key parameters to include:
- `query`: search term from user's selection
- `min_budget`: from user's budget filter
- `full_description`: true
- `job_details`: true
- `limit`: user's count selection
- `sort_field`: time_updated

Run this command to search:
```bash
curl -H "freelancer-oauth-v1: $(grep FREELANCER_OAUTH_TOKEN .env | cut -d= -f2)" \
  "https://www.freelancer.com/api/projects/0.1/projects/active?limit=20&full_description=true&job_details=true&query=YOUR_QUERY" \
  | python3 -m json.tool
```

### Step 4: Score and rank the projects

For each project returned, score it on these dimensions (1–5 each):

| Dimension | What to check |
|-----------|--------------|
| **Skill match** | How well does it match PROFILE.md skills? |
| **Budget** | Is the budget realistic for the scope? |
| **Competition** | How many bids already? (<10 bids = green, >30 = red) |
| **Client quality** | Does client have reviews? Verified payment? |
| **Differentiation** | Can we offer a demo or unique angle? |
| **Win probability** | DACH client? German language? Good brief? |

**Total score = sum of dimensions (max 30)**

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
