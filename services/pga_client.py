#!/usr/bin/env python3
"""
PGA Tour API Client with organic request patterns.

Features:
- Mimics browser requests from pgatour.com
- Randomized rate limiting
- Automatic retry with exponential backoff + jitter
- Respectful of server resources
"""

from __future__ import annotations

import logging
import os
import random
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Optional

import requests

# Handle imports whether run as module or standalone
try:
    from .scheduler import JitteredScheduler, sleep_with_jitter
except ImportError:
    from scheduler import JitteredScheduler, sleep_with_jitter

logger = logging.getLogger(__name__)


def _load_env() -> bool:
    """Load .env file from project root."""
    possible_paths = [
        Path(__file__).parent.parent / ".env",
        Path(__file__).parent / ".env",
        Path.cwd() / ".env",
        Path.cwd().parent / ".env",
    ]
    for env_path in possible_paths:
        if env_path.exists():
            for line in env_path.read_text().strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                # Strip quotes from value if present
                value = value.strip().strip("'\"")
                os.environ.setdefault(key.strip(), value)
            return True
    return False


_load_env()


class PGAClientError(Exception):
    """Base exception for PGA client errors."""
    pass


class PGAClient:
    """GraphQL client for PGA Tour API with organic request patterns."""

    API_URL = "https://orchestrator.pgatour.com/graphql"
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    BASE_RATE_LIMIT = 2.0

    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    ]

    REFERER_PATHS = [
        "https://www.pgatour.com/",
        "https://www.pgatour.com/leaderboard",
        "https://www.pgatour.com/players",
        "https://www.pgatour.com/schedule",
        "https://www.pgatour.com/stats",
        "https://www.pgatour.com/fedexcup",
    ]

    # Position strings that indicate non-finishes
    NON_FINISH_POSITIONS = frozenset({"CUT", "MC", "WD", "DQ", "W/D", "DNS", "MDF"})

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the PGA API client.

        Args:
            api_key: API key (defaults to PGA_TOUR_API_KEY env var)

        Raises:
            ValueError: If no API key is provided or found in environment
        """
        self.api_key = api_key or os.getenv("PGA_TOUR_API_KEY")
        if not self.api_key:
            raise ValueError(
                "PGA_TOUR_API_KEY not set. Provide api_key parameter or set environment variable."
            )

        self.scheduler = JitteredScheduler(base_rate_limit=self.BASE_RATE_LIMIT)
        self._session: Optional[requests.Session] = None
        self._request_count = 0

    @property
    def session(self) -> requests.Session:
        """Lazy-initialize and return the requests session."""
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self) -> None:
        """Close the HTTP session."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> "PGAClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _get_headers(self) -> dict[str, str]:
        """Get request headers mimicking browser from pgatour.com."""
        return {
            "x-api-key": self.api_key,
            "x-pgat-platform": "web",
            "Content-Type": "application/json",
            "Origin": "https://www.pgatour.com",
            "Referer": random.choice(self.REFERER_PATHS),
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=1, i",
        }

    def _safe_get(self, data: Any, *keys: str, default: Any = None) -> Any:
        """
        Safely navigate nested dict structure.

        Handles cases where intermediate values are None.
        """
        result = data
        for key in keys:
            if result is None or not isinstance(result, dict):
                return default
            result = result.get(key)
        return result if result is not None else default

    def query(
        self,
        gql: str,
        variables: Optional[dict] = None,
        retries: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Execute a GraphQL query with organic timing.

        Args:
            gql: GraphQL query string
            variables: Query variables
            retries: Number of retries on failure (defaults to DEFAULT_RETRIES)

        Returns:
            Response data dict

        Raises:
            PGAClientError: On persistent failure after all retries
        """
        if retries is None:
            retries = self.DEFAULT_RETRIES

        self.scheduler.rate_limit_wait()

        payload = {"query": gql}
        if variables:
            payload["variables"] = variables

        last_error: Optional[Exception] = None

        for attempt in range(retries):
            try:
                response = self.session.post(
                    self.API_URL,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.DEFAULT_TIMEOUT,
                )
                response.raise_for_status()
                self._request_count += 1

                try:
                    data = response.json()
                except ValueError as e:
                    raise PGAClientError(f"Invalid JSON response: {e}") from e

                if "errors" in data:
                    logger.warning("GraphQL errors: %s", data["errors"])

                return data

            except requests.exceptions.RequestException as e:
                last_error = e
                logger.warning(
                    "Request failed (attempt %d/%d): %s",
                    attempt + 1,
                    retries,
                    e,
                )

                if attempt < retries - 1:
                    base_wait = (2**attempt) * 5  # 5s, 10s, 20s
                    sleep_with_jitter(base_wait, variance_pct=0.5)

        raise PGAClientError(f"Request failed after {retries} attempts") from last_error

    # ===================
    # Player Queries
    # ===================

    def get_players(self, tour_code: str = "R", active: bool = True) -> list[dict]:
        """
        Get all players for a tour.

        Args:
            tour_code: Tour code (R=PGA, H=Champions, M=Korn Ferry, etc.)
            active: Whether to get only active players

        Returns:
            List of player dicts with id, displayName, country, etc.
        """
        result = self.query(
            """
            query GetPlayers($tourCode: TourCode!, $active: Boolean) {
                playerDirectory(tourCode: $tourCode, active: $active) {
                    players {
                        id
                        firstName
                        lastName
                        displayName
                        country
                        countryFlag
                        headshot
                        isActive
                    }
                }
            }
            """,
            {"tourCode": tour_code, "active": active},
        )
        return self._safe_get(result, "data", "playerDirectory", "players", default=[])

    def get_player_season(
        self, player_id: str, year: int, tour_code: str = "R"
    ) -> dict[str, Any]:
        """
        Get player's season results including earnings.

        Args:
            player_id: Player ID
            year: Season year
            tour_code: Tour code

        Returns:
            Season results with tournaments, earnings, wins, etc.
        """
        result = self.query(
            """
            query GetPlayerSeason($playerId: ID!, $tourCode: TourCode, $year: Int) {
                playerProfileSeasonResults(playerId: $playerId, tourCode: $tourCode, year: $year) {
                    playerId
                    displayYear
                    events
                    wins
                    top10
                    top25
                    cutsMade
                    missedCuts
                    tournaments {
                        tournamentId
                        tournamentName
                        finishPosition
                        total
                        toPar
                        money
                        fedexFallPoints
                        points
                    }
                }
            }
            """,
            {"playerId": player_id, "tourCode": tour_code, "year": year},
        )
        return self._safe_get(result, "data", "playerProfileSeasonResults", default={})

    # ===================
    # Tournament Queries
    # ===================

    def get_schedule(self, tour_code: str = "R", year: str = "2025") -> dict[str, Any]:
        """
        Get tournament schedule.

        Args:
            tour_code: Tour code
            year: Season year (as string)

        Returns:
            Schedule with completed and upcoming tournaments
        """
        result = self.query(
            """
            query GetSchedule($tourCode: String!, $year: String!) {
                schedule(tourCode: $tourCode, year: $year) {
                    seasonYear
                    completed {
                        month
                        year
                        tournaments {
                            id
                            tournamentName
                        }
                    }
                    upcoming {
                        month
                        year
                        tournaments {
                            id
                            tournamentName
                        }
                    }
                }
            }
            """,
            {"tourCode": tour_code, "year": year},
        )
        return self._safe_get(result, "data", "schedule", default={})

    def get_tournament_field(self, tournament_id: str) -> dict[str, Any]:
        """
        Get tournament field (players in the tournament).

        Args:
            tournament_id: Tournament ID (e.g., "R2024016")

        Returns:
            Field data with tournament name and players list
        """
        result = self.query(
            """
            query GetField($id: ID!) {
                field(id: $id) {
                    tournamentName
                    id
                    players {
                        id
                        firstName
                        lastName
                        displayName
                        country
                    }
                }
            }
            """,
            {"id": tournament_id},
        )
        return self._safe_get(result, "data", "field", default={})

    def get_leaderboard(self, tournament_id: str) -> dict[str, Any]:
        """
        Get tournament leaderboard with scoring data.

        Args:
            tournament_id: Tournament ID (e.g., "R2024016")

        Returns:
            Leaderboard with status, rounds, and player scoring data
        """
        result = self.query(
            """
            query GetLeaderboard($id: ID!) {
                leaderboardV3(id: $id) {
                    id
                    tournamentId
                    tournamentStatus
                    leaderboardRoundHeader
                    formatType
                    timezone
                    rounds {
                        roundNumber
                        displayText
                    }
                    players {
                        ... on PlayerRowV3 {
                            id
                            player {
                                id
                                firstName
                                lastName
                                displayName
                                country
                            }
                            scoringData {
                                position
                                total
                                totalSort
                                score
                                thru
                                thruSort
                                rounds
                                playerState
                                groupNumber
                                currentRound
                                official
                                projected
                            }
                        }
                        ... on InformationRow {
                            displayText
                        }
                    }
                }
            }
            """,
            {"id": tournament_id},
        )
        return self._safe_get(result, "data", "leaderboardV3", default={})

    def get_tournament_overview(self, tournament_id: str) -> dict[str, Any]:
        """
        Get tournament overview with purse info.

        Args:
            tournament_id: Tournament ID

        Returns:
            Overview with purse, dates, courses, etc.
        """
        result = self.query(
            """
            query GetTournamentOverview($tournamentId: ID!) {
                tournamentOverview(tournamentId: $tournamentId) {
                    overview {
                        label
                        value
                    }
                    courses {
                        courseName
                        courseId
                    }
                }
            }
            """,
            {"tournamentId": tournament_id},
        )
        return self._safe_get(result, "data", "tournamentOverview", default={})

    # ===================
    # Stats Queries
    # ===================

    def get_stat_leaders(
        self, stat_id: str, year: int = 2024, tour_code: str = "R"
    ) -> dict[str, Any]:
        """
        Get leaders for a specific stat.

        Args:
            stat_id: Stat ID (e.g., "02675" for SG: Total)
            year: Season year
            tour_code: Tour code

        Returns:
            Stat details with title, description, and ranked players
        """
        result = self.query(
            """
            query GetStatDetails($tourCode: TourCode!, $statId: String!, $year: Int) {
                statDetails(tourCode: $tourCode, statId: $statId, year: $year) {
                    statTitle
                    statDescription
                    tourAvg
                    rows {
                        playerId
                        playerName
                        rank
                        value
                    }
                }
            }
            """,
            {"tourCode": tour_code, "statId": stat_id, "year": year},
        )
        return self._safe_get(result, "data", "statDetails", default={})

    def get_fedex_standings(self, year: int = 2025) -> dict[str, Any]:
        """
        Get FedExCup standings.

        Args:
            year: Season year

        Returns:
            FedExCup standings with rankings
        """
        result = self.query(
            """
            query GetTourCup($tour: TourCode!, $year: Int!) {
                tourCups(tour: $tour, year: $year) {
                    id
                    title
                    description
                    rankings {
                        rank
                        rankDiff
                        player {
                            id
                            displayName
                        }
                        points
                        wins
                        top10
                        events
                    }
                }
            }
            """,
            {"tour": "R", "year": year},
        )

        cups = self._safe_get(result, "data", "tourCups", default=[])
        for cup in cups:
            if "FedExCup" in cup.get("title", ""):
                return cup
        return cups[0] if cups else {}

    # ===================
    # Utility Methods
    # ===================

    @staticmethod
    def parse_money(money_str: Optional[str]) -> Decimal:
        """
        Parse '$1,234,567.00' to Decimal.

        Args:
            money_str: Money string like "$1,234,567.00"

        Returns:
            Decimal value (0 if parsing fails)
        """
        if not money_str:
            return Decimal("0")

        cleaned = money_str.replace("$", "").replace(",", "").strip()
        try:
            return Decimal(cleaned)
        except (ValueError, InvalidOperation):
            logger.debug("Failed to parse money string: %s", money_str)
            return Decimal("0")

    @classmethod
    def parse_position(cls, position_str: Optional[str]) -> int:
        """
        Parse '1', 'T5', 'CUT' to numeric (999 for non-finishes).

        Args:
            position_str: Position string like "1", "T5", "CUT"

        Returns:
            Integer position (999 for non-finishes)
        """
        if not position_str:
            return 999

        position_str = position_str.upper().strip()

        if position_str in cls.NON_FINISH_POSITIONS:
            return 999

        cleaned = position_str.replace("T", "").replace(" ", "")
        try:
            return int(cleaned)
        except ValueError:
            logger.debug("Failed to parse position string: %s", position_str)
            return 999

    @property
    def request_count(self) -> int:
        """Get total requests made in this session."""
        return self._request_count

    # Backwards compatibility
    def get_request_count(self) -> int:
        """Get total requests made in this session (deprecated, use request_count property)."""
        return self._request_count


@contextmanager
def pga_client(api_key: Optional[str] = None):
    """
    Context manager for PGAClient.

    Usage:
        with pga_client() as client:
            players = client.get_players()
    """
    client = PGAClient(api_key=api_key)
    try:
        yield client
    finally:
        client.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    with pga_client() as client:
        print("=== PGA Client Test ===\n")

        print("Fetching players...")
        players = client.get_players()
        print(f"Found {len(players)} active players\n")

        print("Fetching leaderboard for R2024016 (The Sentry)...")
        lb = client.get_leaderboard("R2024016")
        print(f"Status: {lb.get('tournamentStatus')}")

        if lb.get("players"):
            for row in lb["players"][:5]:
                if row.get("player"):
                    p = row["player"]
                    s = row["scoringData"]
                    print(f"  {s['position']:3} {p['displayName']:25} {s['total']}")

        print(f"\nTotal requests: {client.request_count}")
