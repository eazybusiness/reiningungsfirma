# PLANNING — Figma → Responsive Website (Portal + Admin)

## Project Overview
Goal: deliver a fully working responsive website within 5 days based on existing Figma layouts (German & English), including:
- Public portal: user login, member management, statistics dashboard for logged-in users
- Admin area: edit user info, manage memberships (signups/paid memberships), statistics by day/week/month/year

## Proposed Approach (5-day delivery)
- Use Figma as the single source of truth for UI.
- Implement a lean backend API with authentication, role-based access (user/admin), and a minimal admin UI.
- Keep the data model simple and extensible (users, memberships, stats events).
- Deliver daily review builds and a short handover session.

## Milestones / Day Plan
### Day 1 — Project setup + auth + base layout
- Repo structure, environments, CI basics
- Responsive layout implementation from Figma exports
- Authentication: register/login/logout + password reset

### Day 2 — Member management (user side)
- Member profile + basic member management UI
- Backend endpoints + validation
- Admin role scaffolding

### Day 3 — Admin: users + memberships
- Admin area (protected)
- Edit user information
- Membership management (status, start/end, paid flag)

### Day 4 — Statistics & reporting
- Logged-in dashboard stats
- Admin reports grouped by day/week/month/year
- Export (CSV) optional if needed

### Day 5 — QA + responsiveness polish + handover
- Cross-device testing (desktop/tablet/mobile)
- Bugfix pass + security pass (auth, permissions)
- Short training + handover notes

## Tech Stack (proposal)
- Frontend: React + TailwindCSS (fast, responsive, maintainable)
- Backend: FastAPI (Python) + PostgreSQL (or SQLite for MVP)
- Auth: secure password hashing + JWT sessions
- Admin: simple role-based UI (admin routes)

## Acceptance Criteria
- Responsive pages match Figma layouts within reason (pixel-perfect where required)
- Users can register/login and view their dashboard
- Admin can manage users and memberships
- Stats available aggregated by time period

## Pricing Notes
- 5-day delivery requires strict scope control.
- Payment provider integration (Stripe/PayPal) can be a follow-up milestone if required.
