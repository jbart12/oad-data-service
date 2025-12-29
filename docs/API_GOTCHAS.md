# PGA Tour API - Gotchas & Important Notes

## 1. Union Types Require Fragments

The `leaderboardV3.players` field returns a **union type** (`PlayerRowV3 | InformationRow`). You MUST use inline fragments:

```graphql
# WRONG - will fail
players {
  player { displayName }
  scoringData { position }
}

# CORRECT
players {
  ... on PlayerRowV3 {
    player { displayName }
    scoringData { position }
  }
  ... on InformationRow {
    displayText
  }
}
```

Other union types include:
- `LeaderboardRowV2` → `PlayerRowV2 | InformationRow`
- `TSPLeaderboardRow` → `TspTeamRow | InformationRow`
- `FieldStatPlayer` → `FieldStatCurrentForm | FieldStatCourseFit`

---

## 2. Parameter Types Are Inconsistent

Different queries expect different types for similar parameters:

| Query | Parameter | Type | Example |
|-------|-----------|------|---------|
| `schedule` | `year` | String | `"2024"` |
| `statOverview` | `year` | Int | `2024` |
| `tourCups` | `year` | Int | `2024` |
| `schedule` | `tourCode` | String | `"R"` |
| `playerDirectory` | `tourCode` | Enum | `R` (no quotes) |
| `statOverview` | `tourCode` | Enum | `R` |

**Rule of thumb**: Check the query documentation if you get type errors.

---

## 3. The `rounds` Field is `[String!]!`

In `LeaderboardScoringDataV3`, the `rounds` field is an array of strings, NOT objects:

```graphql
# WRONG
rounds {
  score
  roundNumber
}

# CORRECT
rounds  # Returns ["67", "65", "66", "65"]
```

---

## 4. Compressed Endpoints

Endpoints ending in `Compressed` (e.g., `leaderboardCompressedV3`) return Base64-encoded, GZIP-compressed JSON:

```python
import base64
import gzip
import json

# response.payload = "H4sIAAAAAAAAA..."
decoded = base64.b64decode(payload)
decompressed = gzip.decompress(decoded)
data = json.loads(decompressed)
```

Same structure as non-compressed versions, just smaller payload.

---

## 5. ID Naming Varies

Query parameters for IDs are inconsistent:

| Query | Parameter Name |
|-------|---------------|
| `field` | `id` |
| `leaderboardV3` | `id` |
| `tournamentOddsV2` | `tournamentId` |
| `scorecardV3` | `tournamentId`, `playerId` |
| `playerProfileSeasonResults` | `playerId` |

---

## 6. Some Fields Are Deprecated

The schema includes deprecated fields. Check for `isDeprecated: true` in the schema. Examples:
- `articleAdConfig` - "use REST API"
- Some `tourcastURL` fields

---

## 7. Subscriptions Are Available

The API supports 56 WebSocket subscriptions for real-time data:
- `onUpdateLeaderboardCompressedV3`
- `onUpdateScorecardCompressedV3`
- `onUpdateTeeTimesCompressedV2`
- `onUpdateOddsToWinMarket`
- etc.

Use these for live tournament tracking.

---

## 8. AWS-Specific Scalar Types

| Type | Format |
|------|--------|
| `AWSDateTime` | `YYYY-MM-DDThh:mm:ss.sssZ` |
| `AWSTimestamp` | Unix timestamp (seconds) |
| `AWSJSON` | JSON string |

---

## 9. Player States

The `PlayerState` enum values:
- `ACTIVE` - Currently playing
- `CUT` - Missed cut
- `WITHDRAWN` - Withdrew
- `DISQUALIFIED` - DQ'd
- `NOT_STARTED` - Not started
- `BETWEEN_ROUNDS` - Between rounds
- `COMPLETE` - Finished tournament

---

## 10. Tournament Status

The `TournamentStatus` enum:
- `NOT_STARTED`
- `IN_PROGRESS`
- `COMPLETED`

---

## 11. Known Rate Limits

**Unknown** - The API doesn't document rate limits. Be conservative with request frequency, especially during live tournaments.

---

## 12. Authentication Notes

- Most read queries work with just the API key
- Mutations like `addFavorites`, `deleteAccount` likely require user authentication
- The API key appears to be a public/shared key for the PGA website

---

## Common Errors

### "Field undefined"
You're using a field that doesn't exist on that type. Check the type documentation.

### "Sub selection not allowed on leaf type"
You're trying to select sub-fields on a scalar. The field is a primitive (String, Int, etc.), not an object.

### "Validation error of type FieldUndefined"
Check that you're using the correct field names. The schema may have different naming than expected.
