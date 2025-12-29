# PGA Tour GraphQL API & Data Service

Complete documentation for the PGA Tour GraphQL API and a Python client for the "One and Done" fantasy golf application.

## Overview

This project provides:
1. **API Documentation** - Complete GraphQL schema documentation generated via introspection
2. **Python Client** - Production-ready API client with organic request patterns
3. **Polling Scheduler** - Human-like request timing to avoid detection

## Quick Start

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
pga/
├── README.md                 # This file
├── .env                      # API key (git-ignored)
├── .gitignore
│
├── services/                 # Python client library
│   ├── README.md             # Client documentation
│   ├── __init__.py           # Package exports
│   ├── pga_client.py         # GraphQL API client
│   └── scheduler.py          # Jittered polling scheduler
│
├── docs/                     # API documentation
│   ├── QUICK_START.md        # Getting started guide
│   ├── API_GOTCHAS.md        # Important quirks
│   ├── DATA_SERVICE_PLAN.md  # Data service architecture
│   ├── queries.md            # All 193 queries
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
└── examples/
    └── queries.py            # Working query examples
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

