# PGA Tour GraphQL API & Data Service

Complete documentation for the PGA Tour GraphQL API and a Python client for the "One and Done" fantasy golf application.

## Overview

This project provides:
1. **API Documentation** - Complete GraphQL schema documentation generated via introspection
2. **Python Client** - Production-ready API client with organic request patterns
3. **Polling Scheduler** - Human-like request timing to avoid detection
4. **Database Schema** - PostgreSQL schema for storing PGA data and game state
5. **Sync Jobs** - Automated data synchronization pipeline
6. **Job Runners** - Scheduled tasks for weekly, daily, and live polling

## Quick Start

### Initial Setup

1. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your PGA_TOUR_API_KEY and DATABASE_URL
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   psql $DATABASE_URL < database/migrations/001_initial_schema.sql
   ```

4. **Run initial sync**:
   ```bash
   python examples/quickstart.py
   ```

### Using the Python Client

```python
from services import PGAClient, pga_client

# Option 1: Context manager (recommended)
with pga_client() as client:
    players = client.get_players()
    leaderboard = client.get_leaderboard("R2024016")
    schedule = client.get_schedule(year="2025")

# Option 2: Manual management
client = PGAClient()
try:
    players = client.get_players()
finally:
    client.close()
```

### Running Sync Jobs

```python
from services.sync import sync_players, sync_schedule, sync_results

# Sync players
result = sync_players(tour_code="R", active_only=True)

# Sync tournament schedule
result = sync_schedule(tour_code="R", year="2025")

# Sync tournament results with earnings
result = sync_results(tournament_id="R2024016", include_earnings=True, year=2024)
```

### Direct GraphQL Queries

```
URL: https://orchestrator.pgatour.com/graphql
Method: POST
Headers:
  x-api-key: <your-api-key>
  x-pgat-platform: web
  Content-Type: application/json
```

```graphql
query {
  leaderboardV3(id: "R2024016") {
    tournamentStatus
    players {
      ... on PlayerRowV3 {
        player { displayName }
        scoringData { position total score rounds }
      }
    }
  }
}
```

## Directory Structure

```
oad-data-service/
├── README.md                 # This file
├── CLAUDE.md                 # Project context for AI assistance
├── config.py                 # Configuration management
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Example environment variables
├── requirements.txt          # Python dependencies
├── .gitignore
│
├── services/                 # Python client library
│   ├── README.md             # Client documentation
│   ├── __init__.py           # Package exports
│   ├── pga_client.py         # GraphQL API client
│   ├── scheduler.py          # Jittered polling scheduler
│   ├── validation.py         # Data validation utilities
│   └── sync/                 # Sync modules
│       ├── __init__.py
│       ├── players.py        # Player sync
│       ├── schedule.py       # Schedule sync
│       ├── results.py        # Results & earnings sync
│       └── leaderboard.py    # Live leaderboard sync
│
├── database/                 # PostgreSQL schema
│   ├── README.md             # Database documentation
│   ├── __init__.py           # Database utilities
│   ├── db.py                 # Connection pooling & helpers
│   └── migrations/
│       └── 001_initial_schema.sql
│
├── jobs/                     # Automated job runners
│   ├── README.md             # Job documentation
│   ├── weekly_sync.py        # Sunday full sync
│   ├── daily_sync.py         # Mon-Wed field updates
│   └── live_poller.py        # Thu-Sun live polling
│
├── docs/                     # Documentation
│   ├── project/              # Internal project docs
│   │   ├── README.md         # Project docs index
│   │   ├── CODE_REVIEW.md    # Code review findings
│   │   ├── IMPROVEMENTS.md   # Improvement summary
│   │   └── QUICK_REFERENCE.md # Quick guide
│   │
│   ├── QUICK_START.md        # API getting started guide
│   ├── API_GOTCHAS.md        # Important API quirks
│   ├── DATA_SERVICE_PLAN.md  # Data service architecture
│   ├── queries.md            # All 193 GraphQL queries
│   ├── mutations.md          # All 64 mutations
│   ├── types.md              # All 744 object types
│   ├── enums.md              # All 94 enum types
│   ├── unions.md             # All 45 union types
│   ├── inputs.md             # All 8 input types
│   ├── scalars.md            # Scalar types
│   └── interfaces.md         # Interface types
│
├── schema/
│   └── schema.json           # Raw GraphQL schema (2.5MB)
│
├── scripts/
│   ├── introspect.py         # Fetch schema via introspection
│   ├── generate_docs.py      # Generate documentation
│   └── explore_api.py        # Explore API endpoints
│
├── examples/
│   ├── queries.py            # Working query examples
│   └── quickstart.py         # Initial setup guide
│
└── logs/                     # Job logs (created automatically)
```

## Services

The `services/` directory contains a production-ready Python client:

### PGAClient

GraphQL client with built-in rate limiting and browser-like headers.

```python
from services import PGAClient, pga_client

with pga_client() as client:
    # Players
    players = client.get_players(tour_code="R", active=True)
    season = client.get_player_season(player_id="52955", year=2024)

    # Tournaments
    schedule = client.get_schedule(year="2025")
    field = client.get_tournament_field("R2024016")
    leaderboard = client.get_leaderboard("R2024016")
    overview = client.get_tournament_overview("R2024016")

    # Stats
    leaders = client.get_stat_leaders(stat_id="02675", year=2024)
    standings = client.get_fedex_standings(year=2025)
```

### Scheduler

Human-like request timing with jitter to avoid detection patterns.

```python
from services import JitteredScheduler, TournamentPhase, TournamentPhaseDetector

scheduler = JitteredScheduler(base_rate_limit=2.0)

# Get polling interval based on tournament phase
phase = TournamentPhaseDetector.get_phase("IN_PROGRESS", current_hour=14)
interval = scheduler.get_live_poll_interval(phase)  # ~3 min with jitter

# Decide whether to poll (adds unpredictability)
if scheduler.should_poll_now(phase):
    # Make request...
    pass
```

See [services/README.md](services/README.md) for complete documentation.

## API Documentation

| File | Description |
|------|-------------|
| [docs/QUICK_START.md](docs/QUICK_START.md) | Quick start guide with common queries |
| [docs/API_GOTCHAS.md](docs/API_GOTCHAS.md) | Important quirks and gotchas |
| [docs/DATA_SERVICE_PLAN.md](docs/DATA_SERVICE_PLAN.md) | Data service architecture |
| [docs/queries.md](docs/queries.md) | All 193 queries with arguments & return types |
| [docs/mutations.md](docs/mutations.md) | All 64 mutations |
| [docs/types.md](docs/types.md) | All 744 object types with fields |
| [docs/enums.md](docs/enums.md) | All 94 enum types with values |
| [docs/unions.md](docs/unions.md) | All 45 union types |
| [docs/inputs.md](docs/inputs.md) | All 8 input types |

## Schema Statistics

| Category | Count |
|----------|-------|
| Queries | 193 |
| Mutations | 64 |
| Object Types | 744 |
| Enum Types | 94 |
| Input Types | 8 |
| Union Types | 45 |
| **Total** | **1,156** |

## Tour Codes

| Code | Tour |
|------|------|
| `R` | PGA TOUR |
| `H` | Champions Tour |
| `M` | Korn Ferry Tour |
| `S` | PGA TOUR Americas |
| `C` | PGA TOUR Canada |
| `E` | DP World Tour |

## ID Formats

| Type | Format | Example |
|------|--------|---------|
| Tournament | `{Tour}{Year}{Num}` | `R2024016` (The Sentry) |
| Player | Numeric string | `52955` (Ludvig Åberg) |
| Tour Cup | `{Tour}-{StatId}-{Year}` | `R-02671-2025` (FedExCup) |
| Stat | Numeric string | `02675` (SG: Total) |

## Key Gotchas

1. **Union Types** - Leaderboard players require inline fragments:
   ```graphql
   players { ... on PlayerRowV3 { player { displayName } } }
   ```

2. **Parameter Types Vary** - Check docs for each query:
   - `schedule(year: "2024")` → String
   - `statOverview(year: 2024)` → Int
   - `playerDirectory(tourCode: R)` → Enum

3. **Compressed Endpoints** - `*Compressed` endpoints return Base64+GZIP JSON

4. **Brotli Compression** - Don't request `br` encoding; use `gzip, deflate` only

## Setup

1. Create `.env` file with your API key:
   ```
   PGA_TOUR_API_KEY=your-api-key
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Test the client:
   ```bash
   python services/pga_client.py
   ```

## Sync Jobs & Automation

### Job Types

1. **Weekly Sync** (`jobs/weekly_sync.py`)
   - **Schedule**: Sundays at 11:00 PM ET
   - **Purpose**: Full data refresh
   - **Operations**: Sync players, schedule, and completed tournament results

2. **Daily Sync** (`jobs/daily_sync.py`)
   - **Schedule**: Mon-Wed at 6:00 AM ET
   - **Purpose**: Update tournament fields
   - **Operations**: Sync upcoming tournament fields, update statuses

3. **Live Poller** (`jobs/live_poller.py`)
   - **Schedule**: Thu-Sun during tournament hours
   - **Purpose**: Real-time leaderboard tracking
   - **Operations**: Adaptive polling based on tournament phase

### Cron Setup

```bash
# Add to crontab (adjust paths as needed)
0 23 * * 0 cd /path/to/oad-data-service && python3 jobs/weekly_sync.py
0 6 * * 1-3 cd /path/to/oad-data-service && python3 jobs/daily_sync.py
*/5 8-20 * * 4-7 cd /path/to/oad-data-service && python3 jobs/live_poller.py
```

### Manual Execution

```bash
# Initial data population
python examples/quickstart.py

# Run individual sync jobs
python jobs/weekly_sync.py
python jobs/daily_sync.py
python jobs/live_poller.py

# Test individual sync operations
python services/sync/players.py
python services/sync/schedule.py
python services/sync/results.py
python services/sync/leaderboard.py
```

## Scripts

```bash
# Test the API client
python services/pga_client.py

# Test the scheduler
python services/scheduler.py

# Run example queries
python examples/queries.py

# Regenerate schema from API
python scripts/introspect.py

# Regenerate documentation
python scripts/generate_docs.py
```

## Database Queries

```sql
-- Check sync status
SELECT operation, status, records_affected, synced_at
FROM sync_log
ORDER BY synced_at DESC
LIMIT 20;

-- View player count
SELECT COUNT(*) FROM players;

-- View recent tournaments
SELECT name, start_date, status, purse
FROM tournaments
ORDER BY start_date DESC
LIMIT 10;

-- Top earners
SELECT p.display_name, SUM(tr.earnings) as total_earnings
FROM tournament_results tr
JOIN players p ON tr.player_id = p.id
GROUP BY p.id, p.display_name
ORDER BY total_earnings DESC
LIMIT 20;

-- Recent leaderboard snapshots
SELECT t.name, ls.player_id, ls.position, ls.total, ls.snapshot_time
FROM leaderboard_snapshots ls
JOIN tournaments t ON ls.tournament_id = t.id
ORDER BY ls.snapshot_time DESC
LIMIT 50;
```

