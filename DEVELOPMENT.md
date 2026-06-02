# Juice WRLD Finder — Development Status

## Current Status: V2 In Progress

### What's Complete (V1 + Early V2)

✅ **Backend (Python FastAPI)**
- 12 database models with relationships
- 17 API endpoints (health, songs, search, eras, producers)
- FastAPI structure: routes, repos, services, models, integrations
- Authentication: JWT-based admin login + API key bot auth
- DownloadLink model with visibility control (public/bot/admin)
- Link management routes: /links, /admin/links, /bot/songs
- Protected admin routes with require_admin dependency
- CORS configured from environment settings
- Discord bot with search and admin commands
- CSV/JSON bulk import tooling
- 90%+ pytest coverage requirements
- GitHub Actions CI pipeline
- Docker Compose for local dev

✅ **Frontend (React SPA - Foundation)**
- Vite + React 18 + TypeScript setup
- Tailwind CSS + PostCSS configured
- API client with axios + JWT interceptor
- useAuth hook for admin authentication
- Dev proxy config (/api → localhost:8000)
- Token storage in localStorage
- Ready for page implementation

✅ **Deployment & DevOps**
- .gitignore (Python, Node, SQLite, .env)
- Dockerfile for backend
- GitHub repository with 3 commits
- Environment variable management (.env.example)
- Project documentation (README, API_SOURCES, REFERENCE_LINKS, TESTING)

---

## What's Next (V2 Completion)

### Phase 1: React Pages (Priority)

**Public Pages:**
- `Gallery.tsx` — Browse/search songs with SearchBar
- `SongDetail.tsx` — Full song metadata + public download links
- `SongCard.tsx` — Reusable card component

**Admin Pages:**
- `admin/Login.tsx` — Username + password login form
- `admin/Dashboard.tsx` — Song list with edit/delete buttons
- `admin/SongEditor.tsx` — Add/edit song form
- `admin/LinkEditor.tsx` — Add/edit/delete download links per song

**Routing & Auth:**
- `router.tsx` — React Router v6 config + PrivateRoute guard
- `App.tsx` — Root layout with navigation
- `main.tsx` — Entry point

### Phase 2: Build & Deploy

**Web Docker & Nginx:**
- `web/Dockerfile` — Multi-stage: Node build → nginx serve
- `web/nginx.conf` — SPA routing fallback + /api proxy
- Update `docker-compose.yml` to include web service

**Testing:**
- Auth route tests (login success/fail, token expiry)
- Link visibility filtering tests (public/bot/admin)
- Bot API key guard tests
- Safety tests (no leaked admin links in public endpoints)

**Documentation:**
- Update README.md with web app instructions
- Add deployment guide for production
- Document password hash generation (bcrypt)

---

## File Structure

```
juice-wrld-finder/
├── app/                        # FastAPI backend
│   ├── api/routes/
│   │   ├── auth.py            # ✅ NEW: JWT login
│   │   ├── links.py           # ✅ NEW: Link CRUD + visibility
│   │   ├── bot.py             # ✅ NEW: Bot API endpoints
│   │   └── admin.py           # ✅ UPDATED: Protected with JWT
│   ├── core/
│   │   ├── auth.py            # ✅ NEW: Password hash + JWT
│   │   ├── config.py          # ✅ UPDATED: Auth settings
│   │   └── security.py        # URL redaction
│   ├── models/
│   │   ├── links.py           # ✅ NEW: DownloadLink + visibility
│   │   └── song.py            # ✅ UPDATED: Added download_links relation
│   ├── main.py                # ✅ UPDATED: CORS + new routes
│   └── ...                     # Other modules unchanged
├── web/                        # ✅ NEW: React SPA
│   ├── src/
│   │   ├── api/client.ts      # ✅ API client + interceptors
│   │   ├── hooks/useAuth.ts   # ✅ Auth hook
│   │   ├── pages/             # 🔄 TO DO: Page components
│   │   ├── components/        # 🔄 TO DO: Shared components
│   │   ├── router.tsx         # 🔄 TO DO: Routes
│   │   └── App.tsx            # 🔄 TO DO: Root
│   ├── package.json           # ✅ Dependencies
│   ├── vite.config.ts         # ✅ Config
│   ├── index.html             # ✅ Entry HTML
│   └── Dockerfile             # 🔄 TO DO: Multi-stage build
├── docker-compose.yml         # 🔄 NEEDS UPDATE: Add web service
├── requirements.txt           # ✅ UPDATED: passlib, pyjwt
└── .github/workflows/ci.yml   # CI pipeline (unchanged)
```

---

## Local Development

### Install Backend Deps

```bash
pip install -r requirements.txt
```

### Set Up Environment

```bash
cp .env.example .env

# Edit .env with:
DISCORD_TOKEN=your_token
ADMIN_PASSWORD_HASH=$(python -c "from app.core.auth import hash_password; print(hash_password('your_password'))")
BOT_API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

Test:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

### Run Frontend (After Pages Done)

```bash
cd web
npm install
npm run dev  # http://localhost:5173
```

The dev proxy will forward `/api/*` to `http://localhost:8000`.

### Docker Full Stack (After Web Complete)

```bash
docker-compose up --build
# API: http://localhost:8000
# Web: http://localhost
```

---

## Security Checklist

✅ Admin routes protected by JWT  
✅ Bot API endpoints protected by API key  
✅ Link visibility enforced at DB query layer  
✅ Public endpoints only return PUBLIC links  
✅ CORS limited to specific origins (not wildcard)  
⚠️ TODO: Test that admin/bot links never leak to public  
⚠️ TODO: Password hash generation guide in docs  
⚠️ TODO: API key rotation strategy  

---

## Next Developer Tasks

1. **Create React pages** (Gallery, SongDetail, Admin Dashboard, LinkEditor)
2. **Add PrivateRoute component** for admin pages
3. **Wire up search and filtering** in Gallery
4. **Test auth flow** (login → token → protected routes)
5. **Create web/Dockerfile** (multi-stage build)
6. **Create web/nginx.conf** (SPA routing + API proxy)
7. **Update docker-compose.yml** to add web service
8. **Write integration tests** for auth/links/bot endpoints
9. **Document password hash generation** in setup guide
10. **Update README.md** with V2 features

---

## Git Commits So Far

1. `b3bbf40` — feat: v1 — FastAPI metadata backend + Discord bot
2. `1d3cd0b` — feat: auth + link visibility model + API key guarding
3. `b39053a` — feat: React SPA scaffold with Vite + Tailwind

---

## Notes for Future Work

- **PostgreSQL Migration (Phase 3):** SQLite works fine for dev/testing. Migrate to PostgreSQL + Redis for production.
- **Test Coverage:** Aim for 90%+ on new auth/links routes.
- **Admin Password:** Use bcrypt CLI or Python script to hash the admin password before deploying.
- **API Key:** Generate a random token and store in `.env`. Rotate regularly in production.
- **JWT Expiry:** Currently 15 minutes. Consider refresh tokens for longer sessions in production.
- **XSS Protection:** JWT stored in localStorage (acceptable for now). Upgrade to httpOnly cookies for production.
