# REQUIREMENTS — Freelance Bid Workspace

> **Purpose:** What this workspace must do, what is deferred, what is out of scope.

---

## Phase 1 (Current): System Foundation

### Must-Have (Done ✅)
- [x] GSD planning structure (`.planning/` folder)
- [x] Profile doc with full skills + positioning
- [x] Workflow: session init (`/init`)
- [x] Workflow: find projects (`/find-projects`)
- [x] Workflow: create bid (`/new-bid`)
- [x] Workspace cleanup (no loose files at root)
- [x] `.env` with `FREELANCER_OAUTH_TOKEN`
- [x] `.gitignore` protecting `.env`

### Must-Have (Next)
- [ ] First API-based project scan + scored shortlist
- [ ] First bid created via `/new-bid` workflow with linked demo
- [ ] Bid tracking system (which bids sent, responses, outcomes)
- [ ] me.hiplus.de updated to "Business Automation Advisor" positioning
- [ ] LinkedIn profile updated (use `freelance_brainstorming/.planning/linkedin_copy_paste.md`)

---

## Phase 2 (Q2 2026): Bid Pipeline Optimization

- [ ] Minimum 10 bids/week using unused monthly credits
- [ ] At least 50% of bids include a linked demo or strategic document
- [ ] Win rate tracking: bids sent vs. projects won
- [ ] Template library for common project types (webapp, Odoo, automation, copywriting)
- [ ] DACH-specific bid language templates (German)

---

## Phase 3 (Q3 2026): Advisory Positioning

- [ ] Advisory bids only (process automation, AI implementation, ERP/CRM)
- [ ] Productized service packages listed on me.hiplus.de
- [ ] Portfolio of completed demos accessible via GitHub Pages
- [ ] Case study documents for top 3 completed projects

---

## Constraints (Hard)

- **Bid length:** 500–700 characters (Freelancer.com limit + winning practice)
- **Each bid in its own subfolder** — no loose files at root
- **No `.env` in git** — secrets stay local
- **Each project folder is self-contained** — shareable via GitHub
- **Never bid below €200/$200** — not worth the overhead

---

## Out of Scope

- Running a full pipeline scheduler (use `freelance_api` project for that)
- Tracking finances/invoicing (separate system)
- Client delivery work (separate project folders outside this workspace)
- Building a SaaS product from this workspace
