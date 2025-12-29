# Sync Jobs

Automated job runners for syncing PGA Tour data.

## Job Types

### 1. Weekly Sync (`weekly_sync.py`)
**Schedule**: Sundays at 11:00 PM ET
**Purpose**: Full data refresh
**Operations**:
- Sync all players (PGA, Champions, Korn Ferry)
- Sync tournament schedule (current + next year)
- Sync completed tournament results with earnings

### 2. Daily Sync (`daily_sync.py`)
**Schedule**: Mon-Wed at 6:00 AM ET
**Purpose**: Update tournament fields for upcoming events
**Operations**:
- Sync tournament fields for upcoming tournaments
- Update tournament status

### 3. Live Poller (`live_poller.py`)
**Schedule**: Thu-Sun during tournament hours
**Purpose**: Real-time leaderboard tracking
**Operations**:
- Poll active tournament leaderboards
- Create leaderboard snapshots
- Update tournament results
- Adaptive polling based on tournament phase

## Scheduling with Cron

Add to crontab:

```bash
# Weekly full sync (Sundays at 11 PM ET)
0 23 * * 0 cd /path/to/oad-data-service && python3 jobs/weekly_sync.py

# Daily field updates (Mon-Wed at 6 AM ET)
0 6 * * 1-3 cd /path/to/oad-data-service && python3 jobs/daily_sync.py

# Live polling (Thu-Sun, 8 AM - 8 PM ET, every 5 minutes)
*/5 8-20 * * 4-7 cd /path/to/oad-data-service && python3 jobs/live_poller.py
```

## Environment Setup

Ensure `.env` file contains:
```
PGA_TOUR_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Logging

All jobs log to:
- Console (stdout/stderr)
- Database `sync_log` table

Check logs:
```sql
SELECT * FROM sync_log ORDER BY synced_at DESC LIMIT 20;
```

## Manual Execution

Run jobs manually for testing:

```bash
# Full weekly sync
python3 jobs/weekly_sync.py

# Daily sync
python3 jobs/daily_sync.py

# Live poll (one iteration)
python3 jobs/live_poller.py
```
