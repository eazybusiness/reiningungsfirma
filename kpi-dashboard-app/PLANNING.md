# KPI Dashboard Application - Planning Document

## Project Overview
Converting Excel-based KPI workbook into a cross-platform dashboard application (web + Windows desktop) with secure outlet-specific access and automated monthly data imports.

## Architecture

### Technology Stack
- **Frontend**: React 18 + TypeScript + Vite
- **UI Components**: Tailwind CSS + shadcn/ui
- **Charts**: Recharts / Apache ECharts
- **State Management**: TanStack Query
- **Backend**: Python FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Data Processing**: Pandas + Pydantic
- **Authentication**: JWT + bcrypt
- **Desktop**: Electron wrapper
- **Deployment**: PWA + Electron installer

### Project Structure
```
kpi-dashboard-app/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Five dashboard tabs
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript definitions
│   │   └── utils/           # Helper functions
│   ├── public/
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # Route handlers
│   │   ├── core/            # Config, security
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Data processing
│   ├── tests/
│   └── requirements.txt
├── desktop/                  # Electron wrapper
│   ├── main.js
│   ├── preload.js
│   └── package.json
├── docs/                     # Documentation
└── shared/                   # Shared types/constants
```

## Core Features

### 1. Five-Tab Dashboard Structure
- Tab 1: Overview (high-level KPIs)
- Tab 2: Sales Performance
- Tab 3: Operational Metrics
- Tab 4: Financial Summary
- Tab 5: Custom Analytics
- All tabs: Interactive charts, filters, drill-downs

### 2. Authentication & Authorization
- Outlet-specific login (outlet ID + password)
- JWT-based session management
- Role-based access control (outlet user vs admin)
- Secure password hashing with bcrypt

### 3. Monthly Data Import
- Admin upload interface (drag-and-drop)
- CSV/Excel file parsing with Pandas
- Data validation before commit
- Import history and rollback capability
- Automatic dashboard refresh after import

### 4. Interactive Visualizations
- Hover tooltips with exact values
- Click-to-drill-down functionality
- Date range filtering
- Chart type variety (line, bar, pie, area, combo)
- Smooth tab switching with data caching

### 5. Cross-Platform Delivery
- Web version (PWA installable)
- Windows desktop app (Electron)
- Single codebase for both
- Auto-update mechanism for desktop

## Development Phases

### Phase 1: Foundation (2 weeks)
- Project scaffolding
- Authentication system
- Basic admin upload
- CSV parsing pipeline
- One sample tab with charts

### Phase 2: Dashboard Completion (3 weeks)
- All five tabs implemented
- Full chart suite
- Interactive features
- Data refresh mechanism

### Phase 3: Desktop Packaging (1.5 weeks)
- Electron configuration
- Windows installer
- PWA manifest
- Performance optimization

### Phase 4: Testing & Deployment (1.5 weeks)
- Unit and E2E tests
- Security audit
- Documentation
- Production deployment

## Coding Standards

### Python (Backend)
- Follow PEP8
- Type hints required
- Google-style docstrings
- Format with black
- Max file length: 500 lines

### TypeScript (Frontend)
- Strict mode enabled
- Functional components with hooks
- Props interfaces for all components
- ESLint + Prettier
- Max file length: 500 lines

### Testing
- Pytest for backend (unit + integration)
- Vitest + React Testing Library for frontend
- Minimum coverage: 80%
- Test files mirror source structure

## Security Considerations
- HTTPS/TLS for all communication
- JWT tokens with expiration
- Password complexity requirements
- SQL injection prevention (parameterized queries)
- XSS protection (React auto-escaping)
- CORS configuration
- Rate limiting on API endpoints
- Audit logging for sensitive operations

## Performance Targets
- Initial page load: < 2 seconds
- Tab switching: < 300ms
- Chart rendering: < 500ms
- File upload processing: < 10 seconds for typical monthly file
- Support 50+ concurrent users (web version)

## Data Model (Preliminary)

### Tables
```sql
outlets
- id (PK)
- name
- password_hash
- created_at
- updated_at

monthly_data
- id (PK)
- outlet_id (FK)
- month
- year
- uploaded_at
- [KPI columns - to be defined from Excel workbook]

import_history
- id (PK)
- filename
- uploaded_by
- uploaded_at
- row_count
- status
```

## Deployment Strategy

### Web Version
- Frontend: Vercel / Netlify
- Backend: Railway / Render
- Database: Managed PostgreSQL
- SSL certificates: Auto-provisioned
- Estimated cost: $20-40/month

### Desktop Version
- Build with electron-builder
- Distribute via download link
- Auto-update from GitHub releases
- No ongoing hosting cost

## Open Questions (Awaiting Client Input)
1. Exact structure of five tabs (chart types, metrics)
2. Sample CSV/Excel file format
3. Number of outlets
4. Monthly data volume (row count)
5. Branding requirements (logo, colors)
6. Hosting preference (cloud vs self-hosted)
7. Custom Excel formulas that need replication

## Constraints
- Must maintain exact feature parity with Excel workbook
- No data visible across outlets (strict isolation)
- Simple monthly upload process (non-technical admin)
- Works on Windows 10/11
- Modern browsers (Chrome, Edge, Firefox - last 2 versions)

## Future Enhancements (Out of Initial Scope)
- PDF/Excel export from dashboards
- Scheduled email reports
- Mobile native apps (iOS/Android)
- API integration with POS systems
- Advanced analytics (forecasting, anomaly detection)
- Multi-language support
