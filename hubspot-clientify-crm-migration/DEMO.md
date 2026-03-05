# DEMO — Migration Checklist (HubSpot → Clientify)

## What I Will Validate in the Audit (Fast)
- Objects in use:
  - Contacts
  - Companies
  - Deals
  - Tickets (if support is used)
  - Custom objects (if any)
- Key properties:
  - Lifecycle stage, lead status, source, owner, tags
  - Custom fields and validation rules
- Pipelines:
  - Number of pipelines, stages, close reasons
- Workflows/Automations:
  - Lead capture → qualification
  - Lead scoring
  - Nurture sequences
  - Deal stage triggers
  - Support routing + SLA rules

## Data Migration Strategy (No-Loss Mindset)
- Backup first:
  - Exports + API snapshot for critical objects
- Transform:
  - Normalize phone/email, handle duplicates
  - Field mapping with controlled fallbacks
- Import:
  - Order of operations to preserve relations:
    1) companies (if needed)
    2) contacts
    3) deals
    4) tickets
    5) activities/notes/tasks (as supported)
- Reconcile:
  - Count checks per object
  - Random sampling across lifecycle stages
  - Edge cases: duplicates, missing emails, merged contacts

## Cutover Plan (Typical)
- Freeze window (optional): stop edits in HubSpot during final run
- Delta sync: import changes made since dry-run
- Go-live verification: dashboards + workflow triggers

## Questions That Decide Complexity
- Does “historial completo” include:
  - email events + thread bodies?
  - call recordings?
  - meeting logs?
  - attachments?
- Do you need a 1:1 replication of workflows, or permission to simplify?
- Any GDPR/consent requirements to preserve for marketing lists?
