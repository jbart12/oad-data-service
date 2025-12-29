# PGA Tour API - Quick Start Guide

## Setup

```python
import requests

API_URL = "https://orchestrator.pgatour.com/graphql"
HEADERS = {
    "x-api-key": "YOUR_API_KEY",
    "x-pgat-platform": "web",
    "Content-Type": "application/json"
}

def query(gql, variables=None):
    payload = {"query": gql}
    if variables:
        payload["variables"] = variables
    return requests.post(API_URL, json=payload, headers=HEADERS).json()
```

---

## Common Queries

### Get All Players
```graphql
query {
  playerDirectory(tourCode: R, active: true) {
    players {
      id
      firstName
      lastName
      displayName
      country
      isActive
    }
  }
}
```

### Get Tournament Schedule
```graphql
query {
  schedule(tourCode: "R", year: "2024") {
    completed {
      tournaments {
        id
        tournamentName
      }
    }
    upcoming {
      tournaments {
        id
        tournamentName
      }
    }
  }
}
```

### Get Leaderboard
```graphql
query {
  leaderboardV3(id: "R2024016") {
    id
    tournamentId
    tournamentStatus
    leaderboardRoundHeader
    players {
      ... on PlayerRowV3 {
        player {
          id
          displayName
          country
        }
        scoringData {
          position
          total
          score
          thru
          rounds
          playerState
          oddsToWin
        }
      }
    }
  }
}
```

### Get Player Season Results
```graphql
query {
  playerProfileSeasonResults(playerId: "52955", tourCode: R, year: 2024) {
    playerId
    displayYear
    events
    wins
    top10
    top25
    cutsMade
    tournaments {
      tournamentId
      tournamentName
      finishPosition
      total
      toPar
      money
    }
  }
}
```

### Get Player Profile
```graphql
query {
  playerProfileOverview(playerId: "52955", currentTour: R) {
    id
    headshot {
      image
      firstName
      lastName
      country
    }
    standings {
      title
      rank
      total
    }
    snapshot {
      title
      value
    }
  }
}
```

### Get Stat Leaders
```graphql
query {
  statOverview(tourCode: R, year: 2024) {
    categories {
      category
      displayName
      subCategories {
        displayName
        stats {
          statId
          statTitle
        }
      }
    }
  }
}
```

### Get Specific Stat Details
```graphql
query {
  statDetails(tourCode: R, statId: "02675", year: 2024) {
    statTitle
    statDescription
    rows {
      playerId
      playerName
      rank
      value
    }
  }
}
```

### Get FedExCup Standings
```graphql
query {
  tourCup(id: "R-02671-2025", type: OFFICIAL) {
    title
    rankings {
      rank
      player { displayName }
      points
    }
  }
}
```

### Get Tournament Field
```graphql
query {
  field(id: "R2024016") {
    tournamentName
    players {
      id
      firstName
      lastName
      country
    }
  }
}
```

### Get Player Scorecard
```graphql
query {
  scorecardV3(tournamentId: "R2024016", playerId: "52955") {
    tournamentName
    player { displayName }
    roundScores {
      roundNumber
      score
      parRelativeScore
    }
  }
}
```

---

## Key Stat IDs

| Stat ID | Name |
|---------|------|
| `02675` | SG: Total |
| `02674` | SG: Tee-to-Green |
| `02567` | SG: Off-the-Tee |
| `02568` | SG: Approach the Green |
| `02569` | SG: Around-the-Green |
| `02564` | SG: Putting |
| `101` | Driving Distance |
| `103` | GIR Percentage |
| `120` | Scoring Average (Adjusted) |
| `02671` | FedExCup Standings |

---

## Tour Codes

| Code | Tour |
|------|------|
| `R` | PGA TOUR |
| `H` | Champions Tour |
| `M` | Korn Ferry Tour |
| `S` | PGA TOUR Americas |
| `C` | PGA TOUR Canada |
| `E` | DP World Tour |

---

## Sample Tournament IDs (2024)

| ID | Tournament |
|----|------------|
| `R2024016` | The Sentry |
| `R2024006` | Sony Open in Hawaii |
| `R2024002` | The American Express |
| `R2024014` | Masters Tournament |
| `R2024033` | PGA Championship |
| `R2024011` | THE PLAYERS Championship |

---

## Sample Player IDs

| ID | Player |
|----|--------|
| `52955` | Ludvig Åberg |
| `33141` | Keegan Bradley |
| `40026` | Daniel Berger |
| `33948` | Byeong Hun An |
| `46046` | Scottie Scheffler |
