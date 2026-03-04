# KPI Dashboard Application

Transform Excel-based KPI workbooks into a modern, cross-platform dashboard application with secure outlet-specific access and automated monthly data imports.

## Overview

This project converts a complex Excel workbook with five KPI-driven tabs into a professional web and desktop application. Each outlet logs in securely to view only their data, and administrators can easily upload monthly CSV/Excel files to refresh all dashboards automatically.

## Key Features

- **Five-Tab Dashboard** - Maintains existing Excel structure for immediate user recognition
- **Secure Access** - Outlet-specific authentication, each location sees only their data
- **Simple Data Refresh** - Drag-and-drop monthly file upload, automatic visualization updates
- **Interactive Charts** - Drill-downs, hover tooltips, date range filtering
- **Cross-Platform** - Web browser access + Windows desktop installation
- **Single Codebase** - Shared code for web and desktop versions simplifies maintenance

## Technology Stack

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- Recharts / Apache ECharts
- TanStack Query

### Backend
- Python FastAPI
- SQLite / PostgreSQL
- Pandas (data processing)
- Pydantic (validation)
- JWT authentication

### Desktop
- Electron wrapper
- Auto-update support
- Windows installer (.exe)

## Project Structure

```
kpi-dashboard-app/
├── frontend/          # React application
├── backend/           # FastAPI server
├── desktop/           # Electron wrapper
├── docs/              # Documentation
├── PROJECT_PROPOSAL.md
├── PLANNING.md
├── TASK.md
└── README.md
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Git

### Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Desktop:**
```bash
cd desktop
npm install
npm run dev
```

## Development Timeline

- **Phase 1**: Foundation (2 weeks) - Auth, upload, sample tab
- **Phase 2**: Dashboard Completion (3 weeks) - All five tabs, full features
- **Phase 3**: Desktop Packaging (1.5 weeks) - Electron, PWA, optimization
- **Phase 4**: Testing & Deployment (1.5 weeks) - Tests, docs, production

**Total: 8 weeks** (part-time) or **4-5 weeks** (full-time)

## Documentation

- [`PROJECT_PROPOSAL.md`](./PROJECT_PROPOSAL.md) - Detailed technical proposal
- [`PLANNING.md`](./PLANNING.md) - Architecture and development plan
- [`TASK.md`](./TASK.md) - Current tasks and backlog
- [`BID_SUMMARY.txt`](./BID_SUMMARY.txt) - 500-character project summary

## Next Steps

1. Client shares Excel workbook for analysis
2. Receive sample CSV/Excel data file
3. Review and finalize technical specifications
4. Begin Phase 1 development

## Contact

For questions or clarifications about this proposal, please reach out to discuss the Excel workbook structure and finalize project scope.

---

**Status**: Awaiting client input (Excel workbook and sample data)  
**Created**: March 4, 2026
