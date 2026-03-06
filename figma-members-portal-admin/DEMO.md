# DEMO — Implementation Notes (Portal + Admin)

## Architecture
- Frontend:
  - Routes: public pages, auth pages, member dashboard, admin area
  - i18n: DE/EN strings based on locale toggle
- Backend:
  - Entities: User, Membership, StatEvent (or DailyStat aggregates)
  - RBAC: user vs admin
  - Reporting endpoints: grouped aggregations by period

## Key Risks (and how to keep 5 days realistic)
- Payments:
  - If payment gateway is required, implement as Phase 2 unless provider is pre-decided and minimal.
- “Statistics” definition:
  - Lock the metrics early (what is counted, from which events).
- Figma export code:
  - Use it as a base, but refactor into components for maintainability.

## Delivery Process
- Daily build/review link
- End-to-end test checklist
- Handover: short training + admin guide
