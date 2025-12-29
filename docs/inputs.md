# PGA Tour GraphQL API - Complete Input Types Reference

**Total Input Types: 8**

---

## ArticleOddsMarketsInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `market` | `HistoricalOddsId!` | Yes | - |  |
| `class` | `String!` | Yes | - |  |

---

## ArticleOddsPlayerInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `playerName` | `String` | No | - |  |
| `playerId` | `String!` | Yes | - |  |

---

## FavoritePlayerInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `ID!` | Yes | - |  |

---

## NotificationTagInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tag` | `String!` | Yes | - |  |

---

## OddsUpdateInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `provider` | `OddsProvider!` | Yes | - |  |
| `oddsFormat` | `OddsFormat!` | Yes | - |  |

---

## RyderCupRankingsQueryInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tournamentId` | `String!` | Yes | - |  |
| `team` | `RankingsTeams!` | Yes | - |  |

---

## ShotCommentaryItemInput

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `hole` | `Int!` | Yes | - |  |
| `shot` | `Int!` | Yes | - |  |
| `strokeId` | `Int!` | Yes | - |  |
| `commentary` | `String!` | Yes | - |  |
| `active` | `Boolean!` | Yes | - |  |

---

## StatDetailEventQuery

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tournamentId` | `String!` | Yes | - |  |
| `queryType` | `StatDetailQueryType!` | Yes | - |  |

---

