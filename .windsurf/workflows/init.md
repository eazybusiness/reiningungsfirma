---
description: Start a new session - read planning files, summarize state, and prepare for work
---

## Session Init Workflow

Run this at the start of every new conversation to restore context and know exactly what to do next.

1. Read `.planning/STATE.md` and summarize: last session date, what was accomplished, what is next.

2. Read `.planning/PROJECT.md` for identity and positioning context.

3. Read `TASK.md` for currently active tasks and pending items.

4. Read `.planning/ROADMAP.md` and identify the current active milestone.

5. Ask the user which of the following they want to do today:
   - Search for new projects to bid on (`/find-projects`)
   - Write a new bid for a specific project (`/new-bid`)
   - Continue work on an existing bid folder
   - Update the planning/profile docs
   - Something else

6. Update `.planning/STATE.md` with today's date and what was discussed at session start.
