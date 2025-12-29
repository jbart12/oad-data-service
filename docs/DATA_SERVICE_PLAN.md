# One and Done - Data Service Plan

## Game Mechanics Summary

- Users select **ONE golfer per tournament**
- Each golfer can only be used **ONCE per season**
- User's score = **sum of their golfers' tournament earnings**
- Strategy: Optimize which golfer to "spend" on which tournament

---

## 1. Critical Data Requirements

### What We MUST Have

| Data | Why | Source Query |
|------|-----|--------------|
| **Players** | Users need to pick from valid players | `playerDirectory` |
| **Schedule** | Know what tournaments exist | `schedule`, `completeSchedule` |
| **Tournament Fields** | Who's playing in each event | `field` |
| **Final Results + Earnings** | **THE SCORING MECHANISM** | `leaderboardV3`, `tournamentPastResults` |
| **Tournament Status** | Know when picks lock, when to score | `leaderboardV3.tournamentStatus` |

### What Enhances the Experience

| Data | Why | Source Query |
|------|-----|--------------|
| Player Stats | Help users make informed picks | `statDetails`, `playerProfileStatsFullV2` |
| Season Results | Current form indicator | `playerProfileSeasonResults` |
| Course History | Player performance at venue | `playerProfileCourseResults` |
| FedExCup Standings | Rankings context | `tourCup` |
| Odds | Market-based expectations | `tournamentOddsV2` |
| Player Comparison | Head-to-head analysis | `playerComparison` |

---

## 2. Database Schema

### Core Tables

```sql
-- Players
CREATE TABLE players (
    id VARCHAR(10) PRIMARY KEY,          -- PGA player ID (e.g., "52955")
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    country_flag VARCHAR(255),
    headshot_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tournaments
CREATE TABLE tournaments (
    id VARCHAR(20) PRIMARY KEY,           -- PGA tournament ID (e.g., "R2024016")
    name VARCHAR(255) NOT NULL,
    season_year INT NOT NULL,
    start_date DATE,
    end_date DATE,
    course_name VARCHAR(255),
    course_id VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    purse DECIMAL(15,2),                  -- Total prize money
    status VARCHAR(20) DEFAULT 'UPCOMING', -- UPCOMING, IN_PROGRESS, COMPLETED
    format_type VARCHAR(50),              -- STROKE_PLAY, MATCH_PLAY, etc.
    picks_lock_time TIMESTAMP,            -- When user picks lock
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tournament Field (who's playing)
CREATE TABLE tournament_fields (
    tournament_id VARCHAR(20) REFERENCES tournaments(id),
    player_id VARCHAR(10) REFERENCES players(id),
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- ACTIVE, CUT, WITHDRAWN, DISQUALIFIED
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tournament_id, player_id)
);

-- Tournament Results (CRITICAL - this is how we score)
CREATE TABLE tournament_results (
    tournament_id VARCHAR(20) REFERENCES tournaments(id),
    player_id VARCHAR(10) REFERENCES players(id),
    position VARCHAR(10),                 -- "1", "T5", "CUT", etc.
    position_numeric INT,                 -- For sorting (1, 5, 999 for CUT)
    total_score VARCHAR(10),              -- "-20", "E", etc.
    total_strokes INT,
    rounds JSONB,                         -- ["67", "65", "66", "65"]
    earnings DECIMAL(15,2) NOT NULL,      -- THE KEY FIELD FOR SCORING
    fedex_points DECIMAL(10,2),
    status VARCHAR(20),                   -- COMPLETE, CUT, WITHDRAWN, DQ
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tournament_id, player_id)
);

-- Player Stats (for user research)
CREATE TABLE player_stats (
    player_id VARCHAR(10) REFERENCES players(id),
    stat_id VARCHAR(10) NOT NULL,
    stat_name VARCHAR(100),
    value VARCHAR(50),
    rank INT,
    season_year INT NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (player_id, stat_id, season_year)
);

-- Player Season Summary
CREATE TABLE player_seasons (
    player_id VARCHAR(10) REFERENCES players(id),
    season_year INT NOT NULL,
    events INT,
    wins INT,
    top_5 INT,
    top_10 INT,
    top_25 INT,
    cuts_made INT,
    missed_cuts INT,
    earnings DECIMAL(15,2),
    fedex_rank INT,
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (player_id, season_year)
);

-- Leaderboard Snapshots (for live tracking during tournaments)
CREATE TABLE leaderboard_snapshots (
    id SERIAL PRIMARY KEY,
    tournament_id VARCHAR(20) REFERENCES tournaments(id),
    player_id VARCHAR(10) REFERENCES players(id),
    position VARCHAR(10),
    total VARCHAR(10),
    today VARCHAR(10),
    thru VARCHAR(10),
    current_round INT,
    projected_earnings DECIMAL(15,2),     -- Estimated based on position
    snapshot_time TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_leaderboard_snapshots_tournament ON leaderboard_snapshots(tournament_id, snapshot_time DESC);
```

### App Tables (for reference)

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    -- ... auth fields
);

-- Leagues/Competitions
CREATE TABLE leagues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    season_year INT NOT NULL,
    created_by INT REFERENCES users(id)
);

-- User Picks (THE CORE GAME TABLE)
CREATE TABLE user_picks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    league_id INT REFERENCES leagues(id),
    tournament_id VARCHAR(20) REFERENCES tournaments(id),
    player_id VARCHAR(10) REFERENCES players(id),
    picked_at TIMESTAMP DEFAULT NOW(),
    earnings DECIMAL(15,2),               -- Copied from results when official
    UNIQUE (user_id, league_id, tournament_id),  -- One pick per tournament
    UNIQUE (user_id, league_id, player_id)       -- Each player only once per season
);

-- User Season Scores (denormalized for performance)
CREATE TABLE user_scores (
    user_id INT REFERENCES users(id),
    league_id INT REFERENCES leagues(id),
    season_year INT NOT NULL,
    total_earnings DECIMAL(15,2) DEFAULT 0,
    tournaments_played INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, league_id, season_year)
);
```

---

## 3. Polling Strategy

### Frequency Matrix

| Data | When | Frequency | Query |
|------|------|-----------|-------|
| **Schedule** | Season start, weekly refresh | Weekly (Sunday) | `schedule` |
| **Players** | Pre-season, weekly refresh | Weekly (Sunday) | `playerDirectory` |
| **Tournament Field** | Mon-Wed before tournament | Daily until picks lock | `field` |
| **Player Stats** | Weekly refresh | Weekly (Monday) | `statDetails` |
| **Leaderboard (live)** | Thu-Sun during tournament | Every 2-5 minutes | `leaderboardV3` |
| **Final Results** | When status = COMPLETED | Once, then verify | `leaderboardV3` |

### Polling Logic Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEKLY (Sunday Night)                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Sync players: playerDirectory(tourCode: R, active: true)    │
│  2. Sync schedule: schedule(tourCode: "R", year: "2025")        │
│  3. Sync stats: statDetails for key stat IDs                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY (Mon-Wed)                               │
├─────────────────────────────────────────────────────────────────┤
│  For upcoming tournament this week:                              │
│  1. Sync field: field(id: tournamentId)                         │
│  2. Sync odds: tournamentOddsV2 (optional)                      │
│  3. Update picks_lock_time based on first tee time              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                DURING TOURNAMENT (Thu-Sun)                       │
├─────────────────────────────────────────────────────────────────┤
│  While tournament.status = 'IN_PROGRESS':                        │
│  1. Every 2-5 min: leaderboardV3(id: tournamentId)              │
│  2. Update leaderboard_snapshots                                 │
│  3. Calculate projected earnings based on position               │
│  4. Check for status changes (CUT, WD)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              POST-TOURNAMENT (Sunday/Monday)                     │
├─────────────────────────────────────────────────────────────────┤
│  When tournament.status = 'COMPLETED':                           │
│  1. Final leaderboardV3 pull                                     │
│  2. Store tournament_results with FINAL earnings                 │
│  3. Update user_picks.earnings from results                      │
│  4. Recalculate user_scores                                      │
│  5. Mark tournament complete                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Service Architecture

### Option A: Simple Cron Jobs (Recommended for MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                         CRON SCHEDULER                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Weekly    │  │    Daily    │  │    Live     │              │
│  │   Sync      │  │    Sync     │  │   Poller    │              │
│  │ (Sun 2am)   │  │  (6am)      │  │ (2-5 min)   │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    PGA API Client                            ││
│  │              (with rate limiting, retry logic)               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      PostgreSQL                              ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Service Components

```python
# services/
├── __init__.py
├── pga_client.py          # API wrapper with rate limiting
├── sync/
│   ├── players.py         # Sync player data
│   ├── schedule.py        # Sync tournament schedule
│   ├── field.py           # Sync tournament fields
│   ├── leaderboard.py     # Sync live/final leaderboards
│   ├── stats.py           # Sync player statistics
│   └── results.py         # Process final results & scoring
├── jobs/
│   ├── weekly_sync.py     # Weekly full sync job
│   ├── daily_sync.py      # Daily pre-tournament sync
│   └── live_poller.py     # Live tournament polling
└── scoring/
    └── calculator.py      # Calculate user scores from results
```

---

## 5. Key Implementation Details

### Money/Earnings Extraction

The most critical data point is **earnings**. From the API:

```graphql
query {
  playerProfileSeasonResults(playerId: "52955", tourCode: R, year: 2024) {
    tournaments {
      tournamentId
      tournamentName
      finishPosition
      money              # <-- THIS IS KEY: "$2,160,000.00"
    }
  }
}
```

Also available in leaderboard data after tournament completion.

**Parsing money strings:**
```python
def parse_money(money_str):
    """Parse '$1,234,567.00' to Decimal"""
    if not money_str:
        return Decimal('0')
    cleaned = money_str.replace('$', '').replace(',', '')
    return Decimal(cleaned)
```

### Tournament Status Flow

```
UPCOMING → IN_PROGRESS → COMPLETED
           │
           ├── Players can be: ACTIVE, CUT, WITHDRAWN, DISQUALIFIED
           │
           └── When COMPLETED, earnings are FINAL
```

### Picks Lock Logic

```python
def get_picks_lock_time(tournament_id):
    """
    Picks should lock before the first tee time on Thursday.
    Usually lock Wednesday night or Thursday early morning.
    """
    tee_times = get_tee_times(tournament_id)
    first_tee = min(tt.tee_time for tt in tee_times)
    # Lock 1 hour before first tee time
    return first_tee - timedelta(hours=1)
```

### Handling Edge Cases

| Scenario | How to Handle |
|----------|---------------|
| Player withdraws before tournament | Remove from available picks, refund if already picked |
| Player withdraws during tournament | Earnings = $0 (or partial if after cut) |
| Player misses cut | Earnings = $0 (or cut line consolation if any) |
| Player disqualified | Earnings = $0 |
| Tournament canceled | No scoring, pick refunded |
| Playoff | Wait for final results with complete earnings |

---

## 6. Polling Rate Recommendations

### Conservative Approach (Recommended)

| Scenario | Rate |
|----------|------|
| Weekly sync | 1 request/second, batch where possible |
| Daily sync | 1 request/second |
| Live polling | Every 3 minutes during active play |
| Off-hours (night) | Every 15-30 minutes or pause |

### Rate Limiting Implementation

```python
class PGAClient:
    def __init__(self):
        self.last_request = 0
        self.min_interval = 1.0  # seconds between requests

    def _rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

    def query(self, gql, variables=None):
        self._rate_limit()
        # ... make request
```

---

## 7. Key Stats for Fantasy Value

These stats help users make picks:

| Stat ID | Name | Fantasy Relevance |
|---------|------|-------------------|
| `02675` | SG: Total | Overall skill indicator |
| `02674` | SG: Tee-to-Green | Ball-striking ability |
| `02564` | SG: Putting | Clutch finishing |
| `120` | Scoring Average | Consistency |
| `138` | Top 10 Finishes | High-floor picks |
| `300` | Victory Leaders | High-ceiling picks |
| `122` | Consecutive Cuts | Reliability |

### Course Fit Factors

For each tournament, consider:
- **Driving Distance** - Long courses favor bombers
- **Accuracy** - Tight courses favor accuracy
- **Putting Surface** - Bermuda vs Bent grass specialists
- **Course History** - Past performance at venue

---

## 8. Live Scoring Feature

### Real-time Projected Earnings

During a tournament, show users projected earnings based on current position:

```python
def calculate_projected_earnings(position, purse, format_type='STROKE_PLAY'):
    """
    Estimate earnings based on current position.
    Standard PGA payout is roughly:
    1st: 18%, 2nd: 10.9%, 3rd: 6.9%, etc.
    """
    PAYOUT_PERCENTAGES = {
        1: 0.18, 2: 0.109, 3: 0.069, 4: 0.049, 5: 0.041,
        6: 0.036, 7: 0.0335, 8: 0.031, 9: 0.029, 10: 0.027,
        # ... continues down
    }

    if position in PAYOUT_PERCENTAGES:
        return purse * Decimal(str(PAYOUT_PERCENTAGES[position]))
    elif position <= 70:
        # Rough estimate for lower positions
        return purse * Decimal('0.002')  # Minimum payout ~0.2%
    else:
        return Decimal('0')  # Missed cut
```

---

## 9. Recommended MVP Scope

### Phase 1: Core Data (Week 1-2)
- [ ] Players table + sync
- [ ] Tournaments table + sync
- [ ] Tournament fields + sync
- [ ] Tournament results + sync
- [ ] Basic scoring calculation

### Phase 2: Live Features (Week 3-4)
- [ ] Live leaderboard polling during tournaments
- [ ] Projected earnings display
- [ ] Real-time position tracking

### Phase 3: Analytics (Week 5+)
- [ ] Player stats sync
- [ ] Course history
- [ ] Odds integration
- [ ] Pick recommendations

---

## 10. File Structure Proposal

```
one-and-done/
├── pga/                          # What we built today
│   ├── docs/
│   ├── schema/
│   ├── scripts/
│   └── examples/
│
├── services/                     # NEW: Data service
│   ├── pga_client.py            # API client with rate limiting
│   ├── sync/
│   │   ├── players.py
│   │   ├── schedule.py
│   │   ├── field.py
│   │   ├── leaderboard.py
│   │   └── results.py
│   ├── jobs/
│   │   ├── weekly_sync.py
│   │   ├── daily_sync.py
│   │   └── live_poller.py
│   └── scoring/
│       └── calculator.py
│
├── database/                     # NEW: Database
│   ├── migrations/
│   ├── models.py
│   └── schema.sql
│
└── api/                          # NEW: Your app's API
    └── ...
```

---

## Next Steps

1. **Choose database** - PostgreSQL recommended
2. **Set up database schema** - Run migrations
3. **Build PGA client** - Wrapper with rate limiting
4. **Implement sync jobs** - Start with players + schedule
5. **Test with real data** - Sync current season
6. **Add live polling** - For active tournaments
7. **Build scoring logic** - Calculate user scores from results
