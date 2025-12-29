# PGA Tour API - Documentation Index

## Getting Started

- **[QUICK_START.md](QUICK_START.md)** - Common queries and setup
- **[API_GOTCHAS.md](API_GOTCHAS.md)** - Important quirks and pitfalls

## API Reference

| Document | Contents |
|----------|----------|
| [queries.md](queries.md) | 193 queries with arguments and return types |
| [mutations.md](mutations.md) | 64 mutations |
| [types.md](types.md) | 744 object types with all fields |
| [enums.md](enums.md) | 94 enum types with values |
| [unions.md](unions.md) | 45 union types |
| [inputs.md](inputs.md) | 8 input types |
| [scalars.md](scalars.md) | 7 scalar types |
| [interfaces.md](interfaces.md) | 1 interface type |

## Quick Links

### Most Used Queries
- `playerDirectory` - Get all players
- `leaderboardV3` - Get tournament leaderboard
- `schedule` - Get tournament schedule
- `playerProfileSeasonResults` - Get player season stats
- `statDetails` - Get stat leaders
- `field` - Get tournament field
- `tourCup` - Get FedExCup standings

### Key Types
- `Player` - Basic player info
- `PlayerRowV3` - Leaderboard player row
- `LeaderboardScoringDataV3` - Scoring data
- `Tournament` - Tournament info
- `TourCupRankingEvent` - Standings info

### Important Enums
- `TourCode` - R, H, M, S, C, E
- `PlayerState` - ACTIVE, CUT, WITHDRAWN, etc.
- `TournamentStatus` - NOT_STARTED, IN_PROGRESS, COMPLETED
- `StatCategory` - STROKES_GAINED, OFF_TEE, PUTTING, etc.
