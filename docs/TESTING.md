# Testing Guide

This project uses **pytest** (backend) and **vitest** (frontend) with 90%+ coverage requirements.

## Quick Start

### Backend Tests (Python/pytest)
```bash
pytest                          # Run all backend tests
pytest --cov=app               # With coverage report
```

### Frontend Tests (React/vitest)
```bash
cd web
npm install                     # First time only
npm test                        # Run all React tests
npm run test:ui                 # Interactive test UI
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_services/test_search_service.py
```

### Run Specific Test

```bash
pytest tests/test_services/test_search_service.py::test_search_exact_match
```

### Run with Markers

```bash
pytest -m "not slow"
```

## Test Structure

```
tests/
├── conftest.py               # Shared fixtures
├── test_api/
│   ├── test_health.py
│   ├── test_songs.py
│   ├── test_search.py
│   └── test_admin.py
├── test_bot/
│   └── test_commands.py
├── test_services/
│   ├── test_search_service.py
│   └── test_fuzzy.py
└── test_safety/
    └── test_no_leak_links.py
```

## Key Test Categories

### API Tests

Test FastAPI routes and endpoints:

- Health check
- Song listing and fetching
- Search endpoints
- Admin endpoints
- Error handling

### Service Tests

Test business logic:

- Song creation and updates
- Search with fuzzy matching
- Alias resolution
- Producer linking
- Random song selection

### Safety Tests

Verify security properties:

- URL redaction works correctly
- MEGA links are never exposed by default
- Admin role checks work
- No unauthorized downloads possible

### Bot Tests

Test Discord bot commands (requires async fixtures):

- Search command returns correct embeds
- Song detail command shows info
- Era listing works
- Admin commands check permissions

## Test Fixtures

All tests use an in-memory SQLite database via the `db` fixture in `conftest.py`:

```python
def test_something(db: Session) -> None:
    repo = SongRepository(db)
    song = repo.create(title="Test", slug="test")
    assert song.id is not None
```

## Coverage Goals

- **Minimum:** 90% code coverage
- **Target:** 95% for safety-critical code (security.py, admin routes)
- **Exclude:** Configuration, migration stubs, main entry point

View coverage:

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Mocking External APIs

For tests that need external API integration:

```python
import respx
from httpx import Response

@respx.mock
async def test_juice_wrld_api():
    respx.get("https://juicewrldapi.com/api/search").mock(
        return_value=Response(200, json=[{"id": "1", "title": "Song"}])
    )
    
    client = JuiceWRLDAPIClient()
    results = await client.search_songs("query")
    assert len(results) == 1
```

## React Testing (Frontend)

Located in `web/src/components/*.test.tsx`, uses **vitest** and **@testing-library/react**.

### Test Structure

```
web/src/
├── components/
│   ├── SongCard.tsx
│   ├── SongCard.test.tsx          # Component tests
│   ├── FilterBar.tsx
│   ├── FilterBar.test.tsx         # Integration tests
│   └── SearchBar.test.tsx         # Input handling tests
└── test/
    └── setup.ts                   # Test environment setup
```

### Running React Tests

```bash
cd web
npm test -- --run                   # Single run
npm run test:ui                     # Interactive UI with file explorer
npm test -- --watch                 # Watch mode (auto-rerun on change)
```

### React Test Examples

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SongCard from './SongCard'

it('renders song title', () => {
  render(<SongCard song={mockSong} />)
  expect(screen.getByText('Lucid Dreams')).toBeInTheDocument()
})

it('handles user interactions', async () => {
  const user = userEvent.setup()
  render(<SearchBar onSearch={vi.fn()} />)
  const input = screen.getByPlaceholderText('Search songs...')
  await user.type(input, 'test')
  expect(input.value).toContain('test')
})
```

## CI/CD

GitHub Actions runs both backend and frontend tests:

### Backend (Python)
```bash
ruff check .       # Linting
mypy app           # Type checking
pytest --cov=app --cov-fail-under=90  # Tests + coverage gate
```

### Frontend (React)
```bash
cd web
npm install        # Install dependencies
npm test -- --run  # Run vitest
npm run build      # Build web app (catches build errors)
```

All must pass before merging to `main`, `develop`, or `master`.

## Tips

1. **Use fixtures for common setup:**
   ```python
   @pytest.fixture
   def populated_db(db):
       repo = SongRepository(db)
       repo.create(title="Song1", slug="song1")
       return db
   ```

2. **Test edge cases:**
   - Empty search queries
   - Songs with no aliases
   - Missing MEGA folders
   - Invalid admin roles

3. **Keep tests fast:**
   - Use in-memory SQLite
   - Mock external APIs
   - Avoid sleep() calls
   - Run in parallel: `pytest -n auto` (with pytest-xdist)

4. **Test the safety properties:**
   - Always test that private URLs are redacted
   - Verify admin checks work
   - Ensure download flags are respected
