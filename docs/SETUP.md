# Setup and Development Guide

Complete setup instructions for local development of the Juice WRLD Finder.

## Prerequisites

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Git** (for version control)
- **npm** (comes with Node.js)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rolling-codes/juice-wrld-finder.git
cd juice-wrld-finder
```

### 2. Backend Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 3. Frontend Setup

```bash
cd web
npm install
cd ..
```

## Configuration

### Environment Variables (`.env`)

Create a `.env` file in the root directory:

```env
# Discord
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
ADMIN_ROLE_ID=your_admin_role_id_here

# Database
DATABASE_URL=sqlite:///./juice_wrld.db
REDIS_URL=redis://localhost:6379

# API
JUICEWRLD_API_BASE=https://juicewrldapi.com/api

# Feature Flags
EXPOSE_API_DOWNLOAD_LINKS=true
EXPOSE_MEGA_LINKS=true

# MEGA Folders
MEGA_MAIN_COMP=https://mega.nz/folder/LU9gWY7Z#PMTqIPB69dT0OW5CiHEizQ
MEGA_ERA_COMP=https://mega.nz/folder/XREQ3A7a#1IYPO9liju-ORDSZs4JJCQ
MEGA_COVER_ART_COMP=https://mega.nz/folder/6B5wmJzL#OeN-JJXayEHfXyLYhLfBkg
MEGA_MEDIA_COMP=https://mega.nz/folder/XU5FUCxJ#gECLcpANW9MkVFZtCfMe3Q
MEGA_SESSION_EDITS_COMP=https://mega.nz/folder/DYZWiBBD#dtXjRHEOJTi2KWYGR2MGew

# Security
SECRET_KEY=your_secret_key_here_change_in_production
ADMIN_USERNAME=admin
BOT_API_KEY=your_bot_api_key_here

# Web App
CORS_ORIGINS=http://localhost:5173
PUBLIC_BASE_URL=http://localhost:8000
```

## Running the Application

### Option 1: Web App + Backend (Full Stack)

**Terminal 1 - Backend API:**
```bash
uvicorn app.main:app --reload
# API runs on http://localhost:8000
# Docs available at http://localhost:8000/docs
```

**Terminal 2 - Discord Bot:**
```bash
python -m app.bot.client
```

**Terminal 3 - Frontend:**
```bash
cd web
npm run dev
# Web app runs on http://localhost:5173
```

### Option 2: Web App Only (No Discord)

**Terminal 1 - Backend API:**
```bash
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd web
npm run dev
```

### Option 3: Discord Bot Only (No Web App)

**Terminal 1 - Backend API:**
```bash
uvicorn app.main:app --reload
```

**Terminal 2 - Discord Bot:**
```bash
python -m app.bot.client
```

## Testing

### Backend Tests
```bash
pytest                              # Run all tests
pytest --cov=app                   # With coverage
pytest -v                          # Verbose output
pytest tests/test_api/            # Single test directory
```

### Frontend Tests
```bash
cd web
npm test                           # Run all tests
npm run test:ui                    # Interactive UI
npm test -- --watch                # Watch mode
```

### All Tests (CI Pipeline)
```bash
# Backend
pytest --cov=app --cov-fail-under=90

# Frontend
cd web && npm test -- --run
```

## Development Workflow

### Adding a New API Endpoint

1. Create route file in `app/api/routes/`
2. Define FastAPI route with proper types
3. Add authentication/authorization if needed
4. Create tests in `tests/test_api/`
5. Register route in `app/main.py`

Example:
```python
# app/api/routes/example.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_session

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/{id}")
async def get_example(id: int, db: Session = Depends(get_session)):
    # Implementation
    return {...}
```

### Adding a New React Component

1. Create component in `web/src/components/`
2. Create test file `ComponentName.test.tsx`
3. Import and use in pages or other components
4. Run tests: `npm test`

Example:
```typescript
// web/src/components/MyComponent.tsx
import React from 'react'

export default function MyComponent() {
  return <div>Hello</div>
}

// web/src/components/MyComponent.test.tsx
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

it('renders hello', () => {
  render(<MyComponent />)
  expect(screen.getByText('Hello')).toBeInTheDocument()
})
```

## Data Seeding

### Import from CSV

Prepare a CSV file with song data:

```csv
title,era,release_status,download_status,official_url,api_download_url,notes,aliases,producers
Lucid Dreams,2018,released,available,https://spotify.com/...,https://juicewrldapi.com/...,Original release,Lucid Dream,Nick Mira
```

Then import:
```bash
python scripts/import_csv.py songs.csv
```

### Load from Juice WRLD API

```bash
python scripts/sync_juiceboard_api.py
```

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate venv if something breaks
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Database Issues
```bash
# Reset database
rm juice_wrld.db
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Node Modules Issues
```bash
cd web
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
- API (8000): `lsof -ti:8000 | xargs kill -9`
- Frontend (5173): `lsof -ti:5173 | xargs kill -9`

## Project Structure

```
juice-wrld-finder/
├── app/                    # FastAPI backend
│   ├── api/               # Route handlers
│   ├── core/              # Configuration, auth, security
│   ├── db/                # Database setup
│   ├── models/            # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── services/          # Business logic
│   ├── integrations/      # External API clients
│   └── bot/               # Discord bot
├── web/                   # React frontend
│   ├── src/
│   │   ├── components/    # React components + tests
│   │   ├── pages/         # Page components
│   │   ├── api/           # API client
│   │   ├── types/         # TypeScript types
│   │   └── test/          # Test setup
│   └── package.json
├── tests/                 # Backend tests
├── scripts/               # Data import scripts
├── docs/                  # Documentation
└── .github/workflows/     # GitHub Actions CI
```

## Resources

- [Backend API Docs](./API_SOURCES.md) — Juice WRLD API integration details
- [Testing Guide](./TESTING.md) — Comprehensive testing documentation
- [Reference Links](./REFERENCE_LINKS.md) — Data sources and external links
- [README](../README.md) — Project overview

## Next Steps

1. Set up environment variables in `.env`
2. Run backend: `uvicorn app.main:app --reload`
3. Run frontend: `cd web && npm run dev`
4. Visit http://localhost:5173
5. Check API docs at http://localhost:8000/docs
