# PGA Tour Data Services

Python client library for the PGA Tour GraphQL API with organic request patterns designed for the "One and Done" fantasy golf application.

## Features

- **Browser-like requests** - Mimics requests from pgatour.com with proper headers
- **Rate limiting** - Jittered delays between requests to avoid detection
- **Automatic retry** - Exponential backoff with jitter on failures
- **Context manager** - Proper session cleanup
- **Type hints** - Full type annotations for IDE support

## Installation

```bash
pip install requests
```

## Quick Start

```python
from services import pga_client

with pga_client() as client:
    # Get all active PGA Tour players
    players = client.get_players()
    print(f"Found {len(players)} players")

    # Get tournament leaderboard
    leaderboard = client.get_leaderboard("R2024016")
    print(f"Status: {leaderboard['tournamentStatus']}")
```

## API Reference

### PGAClient

The main client class for interacting with the PGA Tour API.

#### Constructor

```python
PGAClient(api_key: Optional[str] = None)
```

- `api_key`: API key for authentication. Defaults to `PGA_TOUR_API_KEY` environment variable.

#### Methods

##### Player Methods

```python
# Get all players for a tour
get_players(tour_code: str = "R", active: bool = True) -> list[dict]

# Get player's season results including earnings
get_player_season(player_id: str, year: int, tour_code: str = "R") -> dict
```

##### Tournament Methods

```python
# Get tournament schedule
get_schedule(tour_code: str = "R", year: str = "2025") -> dict

# Get tournament field (players in the tournament)
get_tournament_field(tournament_id: str) -> dict

# Get tournament leaderboard with scoring data
get_leaderboard(tournament_id: str) -> dict

# Get tournament overview with purse info
get_tournament_overview(tournament_id: str) -> dict
```

##### Stats Methods

```python
# Get leaders for a specific stat
get_stat_leaders(stat_id: str, year: int = 2024, tour_code: str = "R") -> dict

# Get FedExCup standings
get_fedex_standings(year: int = 2025) -> dict
```

##### Utility Methods

```python
# Parse money string to Decimal
PGAClient.parse_money("$1,234,567.00") -> Decimal(1234567.00)

# Parse position string to int (999 for non-finishes)
PGAClient.parse_position("T5") -> 5
PGAClient.parse_position("CUT") -> 999

# Get request count for this session
client.request_count -> int
```

#### Raw Query

For custom GraphQL queries:

```python
result = client.query("""
    query GetPlayer($id: ID!) {
        player(id: $id) {
            displayName
            country
        }
    }
""", {"id": "52955"})
```

### JitteredScheduler

Adds randomness to request timing to avoid predictable patterns.

#### Constructor

```python
JitteredScheduler(
    base_rate_limit: float = 2.0,
    distraction_probability: float = 0.10,
    distraction_range: tuple[float, float] = (2.0, 8.0)
)
```

#### Methods

```python
# Wait with jittered rate limiting (called automatically by PGAClient)
scheduler.rate_limit_wait() -> float  # Returns actual wait time

# Add jitter to any interval
JitteredScheduler.jitter(base_seconds: float, variance_pct: float = 0.3) -> float

# Get randomized daily sync time (5-7am by default)
scheduler.get_daily_sync_time(start_hour: int = 5, end_hour: int = 7) -> datetime

# Get randomized weekly sync time (Sunday 1-5am by default)
scheduler.get_weekly_sync_time(start_hour: int = 1, end_hour: int = 5) -> datetime

# Get polling interval based on tournament phase
scheduler.get_live_poll_interval(phase: TournamentPhase) -> float

# Probabilistic decision on whether to poll
scheduler.should_poll_now(phase: TournamentPhase) -> bool
```

### TournamentPhase

Enum for tournament phases that affect polling frequency.

```python
from services import TournamentPhase

TournamentPhase.ACTIVE          # Players on course, ~3 min polling
TournamentPhase.BETWEEN_ROUNDS  # Less frequent, ~10 min polling
TournamentPhase.WEATHER_DELAY   # Very infrequent, ~15 min polling
TournamentPhase.NIGHT           # Minimal polling, ~30 min polling
TournamentPhase.INACTIVE        # Tournament not in progress
```

### TournamentPhaseDetector

Determines tournament phase from status and time.

```python
from services import TournamentPhaseDetector, TournamentPhase

# Automatic detection
phase = TournamentPhaseDetector.get_phase(
    tournament_status="IN_PROGRESS",
    current_hour=14,           # Optional, defaults to now
    round_status="IN_PROGRESS" # Optional
)
# Returns: TournamentPhase.ACTIVE
```

### OrganicRequestPattern

Makes request patterns look more human-like.

```python
from services import JitteredScheduler, OrganicRequestPattern

scheduler = JitteredScheduler()
pattern = OrganicRequestPattern(scheduler)

# Process items in batches with random breaks
results = pattern.batch_with_breaks(
    items=player_ids,
    process_func=client.get_player_season,
    batch_size=5
)

# Randomize task order
tasks = [("players", fetch_players), ("schedule", fetch_schedule)]
shuffled = pattern.shuffle_tasks(tasks)
```

## Examples

### Live Tournament Polling

```python
from services import pga_client, JitteredScheduler, TournamentPhaseDetector
import time

scheduler = JitteredScheduler()

with pga_client() as client:
    while True:
        # Get current tournament status
        lb = client.get_leaderboard("R2025001")
        status = lb.get("tournamentStatus", "UPCOMING")

        # Determine phase and polling interval
        phase = TournamentPhaseDetector.get_phase(status)

        if scheduler.should_poll_now(phase):
            # Process leaderboard data...
            print(f"Updated at {time.strftime('%H:%M:%S')}")

        # Wait before next poll
        interval = scheduler.get_live_poll_interval(phase)
        time.sleep(interval)
```

### Batch Player Data Fetch

```python
from services import pga_client, JitteredScheduler, OrganicRequestPattern

scheduler = JitteredScheduler()
pattern = OrganicRequestPattern(scheduler)

with pga_client() as client:
    # Get all player IDs
    players = client.get_players()
    player_ids = [p["id"] for p in players[:50]]  # First 50

    # Fetch season data with organic timing
    def fetch_season(player_id):
        return client.get_player_season(player_id, year=2024)

    results = pattern.batch_with_breaks(
        items=player_ids,
        process_func=fetch_season,
        batch_size=5
    )
```

### Error Handling

```python
from services import pga_client, PGAClientError

with pga_client() as client:
    try:
        leaderboard = client.get_leaderboard("R2024016")
    except PGAClientError as e:
        print(f"API request failed: {e}")
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PGA_TOUR_API_KEY` | API key for authentication | Yes |

### Rate Limiting Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `base_rate_limit` | 2.0s | Minimum delay between requests |
| `distraction_probability` | 10% | Chance of adding extra delay |
| `distraction_range` | 2-8s | Range for extra delay |

### Polling Intervals by Phase

| Phase | Base Interval | With Jitter |
|-------|---------------|-------------|
| ACTIVE | 180s (3 min) | 108-252s |
| BETWEEN_ROUNDS | 600s (10 min) | 360-840s |
| WEATHER_DELAY | 900s (15 min) | 540-1260s |
| NIGHT | 1800s (30 min) | 1080-2520s |

## Module Exports

```python
from services import (
    # Client
    PGAClient,
    PGAClientError,
    pga_client,

    # Scheduler
    JitteredScheduler,
    OrganicRequestPattern,
    TournamentPhase,
    TournamentPhaseDetector,
    sleep_with_jitter,
)
```

## Testing

```bash
# Test the client
python services/pga_client.py

# Test the scheduler
python services/scheduler.py
```

## Architecture

```
services/
├── __init__.py      # Package exports
├── pga_client.py    # GraphQL client with browser-like headers
├── scheduler.py     # Jittered timing for organic patterns
└── README.md        # This file
```

### Request Flow

1. `PGAClient.query()` is called
2. `JitteredScheduler.rate_limit_wait()` adds random delay
3. Request sent with randomized User-Agent and Referer
4. On failure: exponential backoff with jitter, retry up to 3 times
5. Response parsed and returned

### Header Rotation

The client rotates through:
- 6 different User-Agent strings (Chrome, Safari, mobile)
- 6 different Referer paths (leaderboard, players, schedule, etc.)

This makes requests appear to come from different pages and browsers.
