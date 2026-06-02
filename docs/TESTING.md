# Testing Guide

This project uses **pytest** with 90%+ coverage requirement.

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

## CI/CD

GitHub Actions runs:

```bash
ruff check .       # Linting
mypy app           # Type checking
pytest --cov=app --cov-fail-under=90  # Tests + coverage gate
```

All must pass before merging to `main` or `develop`.

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
