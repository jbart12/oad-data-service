# Claude Context

## Project Overview

This is the **data sync service** for "One and Done" - a fantasy golf app where users pick one golfer per PGA tournament (each golfer usable only once per season). User scores = sum of their golfers' tournament earnings.

This repo handles:
- Fetching data from PGA Tour GraphQL API
- Storing in PostgreSQL database
- NOT the user-facing API (that's a separate repo)

## Current State

### Completed
- [x] PGA Tour GraphQL API fully mapped (193 queries, 744 types)
- [x] Python client with organic request patterns (`services/pga_client.py`)
- [x] Jittered scheduler to avoid detection (`services/scheduler.py`)
- [x] PostgreSQL schema designed and deployed (`database/migrations/`)
- [x] Database running on DigitalOcean (already migrated)

### Not Yet Built
- [ ] Sync jobs to populate database (players, tournaments, results)
- [ ] Live polling during tournaments
- [ ] Cron/scheduler setup

## Key Files

| File | Purpose |
|------|---------|
| `services/pga_client.py` | GraphQL client - use `pga_client()` context manager |
| `services/scheduler.py` | Jittered timing with `TournamentPhase` enum |
| `database/migrations/001_initial_schema.sql` | Full PostgreSQL schema |
| `docs/DATA_SERVICE_PLAN.md` | Architecture and polling strategy |

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

## Next Steps

1. Build sync jobs in `services/sync/`:
   - `players.py` - Sync player directory
   - `schedule.py` - Sync tournament schedule
   - `results.py` - Sync tournament results (earnings)
   - `leaderboard.py` - Live polling during events

2. Create job runners in `jobs/`:
   - `weekly_sync.py` - Full sync on Sundays
   - `daily_sync.py` - Field updates Mon-Wed
   - `live_poller.py` - During tournaments Thu-Sun

## API Gotchas

- Union types need inline fragments: `... on PlayerRowV3 { }`
- Don't request `br` encoding (Brotli) - use `gzip, deflate` only
- `schedule(year:)` takes String, `statDetails(year:)` takes Int
- See `docs/API_GOTCHAS.md` for more
