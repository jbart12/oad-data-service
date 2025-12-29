#!/usr/bin/env python3
"""
Explore gaps in our understanding of the PGA Tour API
"""

import os
import json
import requests
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

API_URL = "https://orchestrator.pgatour.com/graphql"
HEADERS = {
    "x-api-key": os.getenv("PGA_TOUR_API_KEY"),
    "x-pgat-platform": "web",
    "Content-Type": "application/json"
}

def query(gql, variables=None):
    """Execute a GraphQL query."""
    payload = {"query": gql}
    if variables:
        payload["variables"] = variables
    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS)
        result = resp.json()
        if "errors" in result:
            print(f"  GraphQL Error: {result['errors'][0].get('message', result['errors'])}")
        return result
    except Exception as e:
        print(f"  Request error: {e}")
        return {"errors": [{"message": str(e)}]}

def explore():
    gaps = {}

    # 1. What tournaments are available? (Need IDs for most queries)
    print("=" * 60)
    print("1. EXPLORING TOURNAMENT IDS")
    print("=" * 60)
    result = query("""
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
    """)
    if result and "data" in result and result["data"] and result["data"].get("schedule"):
        schedule = result["data"]["schedule"]
        completed = schedule.get("completed", [])
        upcoming = schedule.get("upcoming", [])

        print(f"\nCompleted tournaments in 2024: {len(completed)}")
        if completed:
            for week in completed[:5]:
                for t in week.get("tournaments", []):
                    print(f"  - {t['id']}: {t['tournamentName']}")

        print(f"\nUpcoming tournaments: {len(upcoming)}")
        if upcoming:
            for week in upcoming[:3]:
                for t in week.get("tournaments", []):
                    print(f"  - {t['id']}: {t['tournamentName']}")
                    gaps["sample_tournament_id"] = t["id"]
    else:
        print("Error:", result)

    # 2. What stat IDs are available?
    print("\n" + "=" * 60)
    print("2. EXPLORING STAT IDS")
    print("=" * 60)
    result = query("""
        query {
            statOverview(tourCode: R, year: 2024) {
                tourCode
                year
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
    """)
    if result and "data" in result and result["data"] and result["data"].get("statOverview"):
        overview = result["data"]["statOverview"]
        print(f"\nStat categories for {overview['year']}:")
        for cat in overview.get("categories", []):
            print(f"\n  {cat['displayName']} ({cat['category']}):")
            for sub in cat.get("subCategories", [])[:2]:
                print(f"    {sub['displayName']}:")
                for stat in sub.get("stats", [])[:3]:
                    print(f"      - {stat['statId']}: {stat['statTitle']}")
    else:
        print("Error:", result)

    # 3. How do compressed endpoints work?
    print("\n" + "=" * 60)
    print("3. EXPLORING COMPRESSED ENDPOINT FORMAT")
    print("=" * 60)

    # Use a known tournament ID
    current_tournament_id = "R2024016"  # The American Express 2024
    print(f"Using tournament ID: {current_tournament_id}")

    result = query("""
        query GetLeaderboard($id: ID!) {
            leaderboardCompressedV3(id: $id) {
                id
                payload
            }
        }
    """, {"id": current_tournament_id})

    if result and "data" in result and result["data"] and result["data"].get("leaderboardCompressedV3"):
        lb = result["data"]["leaderboardCompressedV3"]
        payload = lb.get("payload", "")
        print(f"\nCompressed payload length: {len(payload)} chars")
        print(f"Payload preview (first 200 chars): {payload[:200]}...")

        # Try to decode
        import base64
        try:
            decoded = base64.b64decode(payload)
            print(f"\nDecoded length: {len(decoded)} bytes")
            # Try to decompress if it's gzipped
            import gzip
            try:
                decompressed = gzip.decompress(decoded)
                json_data = json.loads(decompressed)
                print(f"Decompressed JSON keys: {list(json_data.keys())[:10]}")
            except:
                # Maybe it's just JSON
                try:
                    json_data = json.loads(decoded)
                    print(f"Decoded JSON keys: {list(json_data.keys())[:10]}")
                except:
                    print(f"Decoded bytes (first 100): {decoded[:100]}")
        except Exception as e:
            print(f"Base64 decode error: {e}")
    else:
        print("Error or no data:", result.get("errors", result))

    # 4. What player IDs look like
    print("\n" + "=" * 60)
    print("4. EXPLORING PLAYER ID FORMAT")
    print("=" * 60)
    result = query("""
        query {
            playerDirectory(tourCode: R, active: true) {
                players {
                    id
                    displayName
                    country
                }
            }
        }
    """)
    if result and "data" in result and result["data"] and result["data"].get("playerDirectory"):
        players = result["data"]["playerDirectory"]["players"]
        print(f"\nTotal active players: {len(players)}")
        print("\nSample player IDs:")
        for p in players[:10]:
            print(f"  - {p['id']}: {p['displayName']} ({p['country']})")
    else:
        print("Error:", result)

    # 5. Tour Cup / FedEx Cup IDs
    print("\n" + "=" * 60)
    print("5. EXPLORING TOUR CUP IDS")
    print("=" * 60)
    result = query("""
        query {
            tourCups(tour: R, year: 2024) {
                id
                title
                description
            }
        }
    """)
    if result and "data" in result and result["data"] and result["data"].get("tourCups"):
        cups = result["data"]["tourCups"]
        print(f"\nTour cups for 2024:")
        for cup in cups:
            print(f"  - {cup['id']}: {cup['title']}")
            if cup.get("description"):
                print(f"    {cup['description'][:100]}")
    else:
        print("Error:", result)

    # 6. Odds providers and format
    print("\n" + "=" * 60)
    print("6. EXPLORING ODDS DATA")
    print("=" * 60)
    result = query("""
        query {
            tournamentOddsV2(tournamentId: "R2024016", provider: FANDUEL, oddsFormat: MONEYLINE) {
                id
                provider
                round
                markets {
                    marketId
                    marketTitle
                }
            }
        }
    """)
    if result and "data" in result and result["data"] and result["data"].get("tournamentOddsV2"):
        odds = result["data"]["tournamentOddsV2"]
        print(f"\nOdds data for tournament:")
        print(f"  Provider: {odds['provider']}")
        print(f"  Round: {odds['round']}")
        print(f"  Markets:")
        for m in odds.get("markets", [])[:5]:
            print(f"    - {m['marketId']}: {m['marketTitle']}")
    else:
        print("No odds data or error:", result.get("errors", "No data"))

    # 7. Field stat types
    print("\n" + "=" * 60)
    print("7. EXPLORING FIELD STATS")
    print("=" * 60)
    for stat_type in ["CURRENT_FORM", "TOURNAMENT_HISTORY", "COURSE_FIT"]:
        result = query("""
            query GetFieldStats($tournamentId: ID!, $fieldStatType: FieldStatType) {
                fieldStats(tournamentId: $tournamentId, fieldStatType: $fieldStatType) {
                    tournamentId
                    fieldStatType
                    statHeaders {
                        displayName
                    }
                }
            }
        """, {"tournamentId": "R2024016", "fieldStatType": stat_type})
        if result and "data" in result and result["data"] and result["data"].get("fieldStats"):
            fs = result["data"]["fieldStats"]
            headers = [h["displayName"] for h in fs.get("statHeaders", [])]
            print(f"\n  {stat_type}: {headers}")
        else:
            print(f"\n  {stat_type}: No data")

    # 8. What subscriptions are available?
    print("\n" + "=" * 60)
    print("8. CHECKING SUBSCRIPTIONS")
    print("=" * 60)

    # Look for subscription type in our schema
    with open("pga_schema_raw.json") as f:
        schema = json.load(f)

    sub_type = schema.get("subscriptionType")
    if sub_type:
        sub_name = sub_type.get("name")
        for t in schema.get("types", []):
            if t["name"] == sub_name:
                print(f"Subscription type: {sub_name}")
                for field in t.get("fields", []):
                    print(f"  - {field['name']}")
                break
    else:
        print("No subscription type found in schema")

    print("\n" + "=" * 60)
    print("SUMMARY OF UNKNOWNS")
    print("=" * 60)

if __name__ == "__main__":
    explore()
