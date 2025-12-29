#!/usr/bin/env python3
"""
PGA Tour API - Working Query Examples

Usage:
    python examples/queries.py
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
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    return response.json()


def get_all_players():
    """Get all active PGA Tour players."""
    result = query("""
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
    """)
    return result.get("data", {}).get("playerDirectory", {}).get("players", [])


def get_schedule(year="2024"):
    """Get tournament schedule for a year."""
    result = query("""
        query GetSchedule($year: String!) {
            schedule(tourCode: "R", year: $year) {
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
    """, {"year": year})
    return result.get("data", {}).get("schedule", {})


def get_leaderboard(tournament_id):
    """Get leaderboard for a tournament."""
    result = query("""
        query GetLeaderboard($id: ID!) {
            leaderboardV3(id: $id) {
                id
                tournamentId
                tournamentStatus
                leaderboardRoundHeader
                formatType
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
                        }
                    }
                }
            }
        }
    """, {"id": tournament_id})
    return result.get("data", {}).get("leaderboardV3", {})


def get_player_season(player_id, year=2024):
    """Get player's season results."""
    result = query("""
        query GetPlayerSeason($playerId: ID!, $year: Int) {
            playerProfileSeasonResults(playerId: $playerId, tourCode: R, year: $year) {
                playerId
                displayYear
                events
                wins
                top10
                top25
                cutsMade
                tournaments {
                    tournamentName
                    finishPosition
                    total
                    toPar
                    money
                }
            }
        }
    """, {"playerId": player_id, "year": year})
    return result.get("data", {}).get("playerProfileSeasonResults", {})


def get_stat_leaders(stat_id, year=2024):
    """Get leaders for a specific stat."""
    result = query("""
        query GetStatDetails($statId: String!, $year: Int) {
            statDetails(tourCode: R, statId: $statId, year: $year) {
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
    """, {"statId": stat_id, "year": year})
    return result.get("data", {}).get("statDetails", {})


def get_fedex_standings():
    """Get current FedExCup standings."""
    result = query("""
        query {
            tourCups(tour: R, year: 2024) {
                id
                title
                description
            }
        }
    """)
    return result.get("data", {}).get("tourCups", [])


def get_tournament_field(tournament_id):
    """Get field for a tournament."""
    result = query("""
        query GetField($id: ID!) {
            field(id: $id) {
                tournamentName
                players {
                    id
                    firstName
                    lastName
                    country
                }
            }
        }
    """, {"id": tournament_id})
    return result.get("data", {}).get("field", {})


# Demo functions
def demo_leaderboard():
    """Demo: Show leaderboard for The Sentry 2024."""
    print("\n=== LEADERBOARD: The Sentry 2024 ===")
    lb = get_leaderboard("R2024016")
    if lb:
        print(f"Status: {lb.get('tournamentStatus')}")
        print(f"Round: {lb.get('leaderboardRoundHeader')}")
        print(f"\n{'Pos':4} {'Player':28} {'Total':6} {'Rounds'}")
        print("-" * 60)
        for row in lb.get("players", [])[:15]:
            if row.get("player"):
                p = row["player"]
                s = row["scoringData"]
                rounds = "/".join(s.get("rounds", []))
                print(f"{s['position']:4} {p['displayName']:28} {s['total']:6} {rounds}")


def demo_player_season():
    """Demo: Show Ludvig Åberg's 2024 season."""
    print("\n=== PLAYER SEASON: Ludvig Åberg 2024 ===")
    season = get_player_season("52955", 2024)
    if season:
        print(f"Events: {season.get('events')}")
        print(f"Wins: {season.get('wins')}")
        print(f"Top 10s: {season.get('top10')}")
        print(f"Cuts Made: {season.get('cutsMade')}")
        print(f"\n{'Pos':5} {'Tournament':35} {'Score':8} {'Money'}")
        print("-" * 70)
        for t in season.get("tournaments", [])[:10]:
            print(f"{t['finishPosition']:5} {t['tournamentName'][:35]:35} {t['toPar']:8} {t['money']}")


def demo_stat_leaders():
    """Demo: Show SG: Total leaders."""
    print("\n=== STAT LEADERS: Strokes Gained Total ===")
    stats = get_stat_leaders("02675", 2024)
    if stats:
        print(f"Stat: {stats.get('statTitle')}")
        print(f"\n{'Rank':5} {'Player':28} {'Value'}")
        print("-" * 45)
        for row in stats.get("rows", [])[:15]:
            print(f"{row['rank']:5} {row['playerName']:28} {row['value']}")


if __name__ == "__main__":
    if not HEADERS["x-api-key"]:
        print("ERROR: Set PGA_TOUR_API_KEY environment variable")
        exit(1)

    demo_leaderboard()
    demo_player_season()
    demo_stat_leaders()
