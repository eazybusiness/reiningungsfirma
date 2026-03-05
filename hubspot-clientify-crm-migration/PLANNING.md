# PLANNING — HubSpot → Clientify Migration

## Project Overview
The client wants to replace their current HubSpot instance with Clientify, with a clean migration that preserves data and sales history, replicates (and improves) automations/workflows, and sets up three areas in Clientify:
- Marketing automation
- Sales management
- Customer support

## Proposed Approach
- Map the current HubSpot data model (objects + custom properties), pipelines, and workflows.
- Define the target model in Clientify (fields, pipelines, tags, ownership rules).
- Migrate in controlled phases with backups, dry-runs, and reconciliation.
- Rebuild automations with a focus on simplification and scalability.
- Validate with sampling + edge cases (duplicates, missing emails, lifecycle stages).

## Milestones (3–5)
### Milestone 1 — Audit + Migration Blueprint (1–2 days)
Deliverables:
- Inventory of HubSpot objects/fields/pipelines/workflows
- Data mapping document (HubSpot → Clientify)
- Migration plan with risks, rollback, and acceptance criteria

### Milestone 2 — Data Backup + Dry-Run Migration (1–2 days)
Deliverables:
- Full exports/backups (contacts, companies, deals, activities as available)
- Test import into Clientify (subset)
- Reconciliation report (counts + spot checks)

### Milestone 3 — Production Migration (1–3 days)
Deliverables:
- Final migration run
- Associations validation (e.g., deal ↔ contact/company)
- Delta sync approach if cutover requires a freeze window

### Milestone 4 — Rebuild/Improve Automations + Sales & Support Setup (2–5 days)
Deliverables:
- Sales pipelines/stages/products configured
- Marketing workflows (email sequences, scoring, nurturing)
- Support dashboards/reports

### Milestone 5 — QA + Training + Post-Go-Live Support (1–2 days + optional support window)
Deliverables:
- Test protocol + fixes
- Short training session + SOP notes
- Post-migration support for fine-tuning

## Tools / Tech
- HubSpot exports + HubSpot REST API (as needed)
- Clientify imports + Clientify API (as needed)
- Python scripts for transformation + reconciliation (repeatable, logged)

## Pricing / Estimate
- Budget range: €250–750.
- Recommended scoping: fixed scope for audit + core migration, then optional add-on for advanced activity history/email events if the platforms require custom ETL.

## What Makes This Bid Unique
- Risk-first migration: backups, dry-runs, reconciliation report, acceptance criteria.
- Focus on simplification: workflows rebuilt to be maintainable and scalable.
- Business context: Sales Ops + process optimization (not only “data moving”).
