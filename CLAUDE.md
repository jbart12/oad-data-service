# Claude Context

## Project Overview

This is the **data sync service** for "One and Done" - a fantasy golf app where users pick one golfer per PGA tournament (each golfer usable only once per season). User scores = sum of their golfers' tournament earnings.

This repo handles:
- Fetching data from PGA Tour GraphQL API
- Storing in PostgreSQL database
- NOT the user-facing API (that's a separate repo)

## Current State

### Completed ✅
- [x] PGA Tour GraphQL API fully mapped (193 queries, 744 types)
- [x] Python client with organic request patterns (`services/pga_client.py`)
- [x] Jittered scheduler to avoid detection (`services/scheduler.py`)
- [x] PostgreSQL schema designed and deployed (`database/migrations/`)
- [x] Database running on DigitalOcean (already migrated)
- [x] **Sync jobs implemented** (`services/sync/`)
- [x] **Job runners created** (`jobs/`)
- [x] **Configuration management** (`config.py`)
- [x] **Data validation utilities** (`services/validation.py`)
- [x] **Enhanced database module** with retry logic and health checks
- [x] **Code review completed** - see `docs/project/`

### Ready for Deployment 🚀
- All core functionality implemented
- Production-ready with proper error handling
- Comprehensive logging and monitoring hooks
- Zero breaking changes from improvements

## Key Files

| File | Purpose |
|------|---------|
| `services/pga_client.py` | GraphQL client - use `pga_client()` context manager |
| `services/scheduler.py` | Jittered timing with `TournamentPhase` enum |
| `services/sync/` | Sync modules (players, schedule, results, leaderboard) |
| `database/db.py` | Enhanced database utilities with retry & validation |
| `database/migrations/001_initial_schema.sql` | Full PostgreSQL schema |
| `config.py` | Centralized configuration management |
| `services/validation.py` | Data validation utilities |
| `jobs/` | Automated job runners (weekly, daily, live poller) |
| `docs/DATA_SERVICE_PLAN.md` | Architecture and polling strategy |
| `docs/project/` | **Internal project documentation** |

## Usage

```python
from services import pga_client

with pga_client() as client:
    players = client.get_players()
    leaderboard = client.get_leaderboard("R2024016")
```

## Environment Variables

Stored in `.env` (git-ignored):
- `PGA_TOUR_API_KEY` - PGA Tour API key
- `DATABASE_URL` - PostgreSQL connection string (DigitalOcean managed DB)

## Database

- **Host**: DigitalOcean managed PostgreSQL
- **Tables**: 13 tables (players, tournaments, results, picks, etc.)
- **Schema**: See `database/README.md`

## API Gotchas

- Union types need inline fragments: `... on PlayerRowV3 { }`
- Don't request `br` encoding (Brotli) - use `gzip, deflate` only
- `schedule(year:)` takes String, `statDetails(year:)` takes Int
- See `docs/API_GOTCHAS.md` for more

## Documentation Guidelines

### Where to Put Documentation Files

**IMPORTANT**: Do NOT create .md files in the project root - they clutter the directory.

| Type | Location | Examples |
|------|----------|----------|
| **Internal project docs** | `docs/project/` | Code reviews, improvements, architecture decisions |
| **API documentation** | `docs/` | GraphQL schema docs, query examples, API gotchas |
| **Code-level docs** | Inline docstrings | Function/class documentation |
| **User-facing docs** | `README.md` only | Setup, usage, quick start |

### Creating New Documentation

When adding project documentation (code reviews, design docs, etc.):

```bash
# Create files in docs/project/
touch docs/project/my-document.md

# NOT in the root
# ❌ touch MY_DOCUMENT.md  # Don't do this!
```

### Existing Documentation Structure

```
docs/
├── project/              # Internal project documentation
│   ├── README.md         # Index of project docs
│   ├── CODE_REVIEW.md    # Code review findings
│   ├── IMPROVEMENTS.md   # Summary of improvements
│   └── QUICK_REFERENCE.md # Quick guide
│
├── API_GOTCHAS.md        # PGA API quirks
├── DATA_SERVICE_PLAN.md  # Architecture
├── QUICK_START.md        # API quick start
├── queries.md            # GraphQL queries
├── types.md              # GraphQL types
└── ... (other API docs)
```

## Recent Improvements (2025-01)

- **Database Module**: Added retry logic, health checks, enhanced validation
- **Configuration**: Centralized config with environment variable support
- **Validation**: Comprehensive data validation utilities
- **Error Handling**: Custom exceptions with better error messages
- See `docs/project/QUICK_REFERENCE.md` for details
