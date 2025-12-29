# Database

PostgreSQL database schema for the PGA data sync service.

## Setup

### 1. Create Database

```bash
createdb pga_data
```

### 2. Run Migrations

```bash
psql -d pga_data -f database/migrations/001_initial_schema.sql
```

Or with connection string:

```bash
psql $DATABASE_URL -f database/migrations/001_initial_schema.sql
```

## Schema Overview

### Core PGA Tables

| Table | Description |
|-------|-------------|
| `players` | PGA Tour player directory |
| `tournaments` | Tournament schedule |
| `tournament_fields` | Players registered for each tournament |
| `tournament_results` | Final results with earnings (scoring source) |
| `player_stats` | Player statistics by season |
| `player_seasons` | Season summary per player |
| `leaderboard_snapshots` | Live scoring snapshots during tournaments |

### App Tables

| Table | Description |
|-------|-------------|
| `users` | User accounts |
| `leagues` | Competition groups |
| `league_members` | League membership |
| `user_picks` | Player selections per tournament (core game table) |
| `user_scores` | Aggregated scores per user/league/season |

### Utility Tables

| Table | Description |
|-------|-------------|
| `sync_log` | Track sync operations for monitoring |

## Key Constraints

### One and Done Rules

The `user_picks` table enforces the game rules:

```sql
UNIQUE (user_id, league_id, tournament_id)  -- One pick per tournament
UNIQUE (user_id, league_id, player_id)      -- Each player only once per season
```

### Scoring

User scores are calculated from `tournament_results.earnings`:

```sql
SELECT
    up.user_id,
    up.league_id,
    SUM(tr.earnings) as total_score
FROM user_picks up
JOIN tournament_results tr
    ON tr.tournament_id = up.tournament_id
    AND tr.player_id = up.player_id
WHERE tr.is_official = true
GROUP BY up.user_id, up.league_id;
```

## Migrations

| Migration | Description |
|-----------|-------------|
| `001_initial_schema.sql` | Initial schema with all tables |

### Running a Migration

```bash
psql -d pga_data -f database/migrations/001_initial_schema.sql
```

### Rolling Back

Each migration should have a corresponding rollback. For the initial schema:

```bash
psql -d pga_data -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

## Indexes

Key indexes for performance:

- `idx_tournaments_status` - Filter active tournaments
- `idx_results_earnings` - Leaderboard sorting
- `idx_picks_user_league` - User pick lookups
- `idx_snapshots_tournament_time` - Live leaderboard queries

## Triggers

Auto-update `updated_at` timestamps on all tables with that column.
