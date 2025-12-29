"""
Tournament results synchronization.

Syncs tournament results (including earnings) from PGA Tour API to the database.
This is CRITICAL for the scoring system - user scores = golfer earnings.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal, InvalidOperation

from ..pga_client import pga_client
from database import upsert_records, log_sync, execute_dict_query

logger = logging.getLogger(__name__)


def _parse_money(money_str: Optional[str]) -> Decimal:
    """
    Parse money string to Decimal.

    Args:
        money_str: Money string (e.g., "$1,234,567" or "1234567")

    Returns:
        Decimal value (0 if unparseable)
    """
    if not money_str:
        return Decimal("0")

    try:
        # Remove $, commas, and whitespace
        cleaned = str(money_str).replace("$", "").replace(",", "").strip()
        return Decimal(cleaned) if cleaned else Decimal("0")
    except (ValueError, InvalidOperation):
        logger.warning(f"Could not parse money: {money_str}")
        return Decimal("0")


def _parse_position(position_str: Optional[str]) -> tuple[str, Optional[int]]:
    """
    Parse position string to (string, numeric) tuple.

    Args:
        position_str: Position string (e.g., "1", "T5", "CUT")

    Returns:
        Tuple of (position_string, numeric_position or None)
    """
    if not position_str:
        return ("", None)

    position_str = str(position_str).strip()

    # Handle special positions (CUT, WD, etc.)
    if position_str.upper() in ("CUT", "MC", "WD", "DQ", "W/D", "DNS", "MDF"):
        return (position_str.upper(), None)

    # Try to extract numeric value (handles "T5", "5", etc.)
    try:
        # Remove 'T' prefix if present
        numeric_str = position_str.lstrip("T").strip()
        numeric_val = int(numeric_str)
        return (position_str, numeric_val)
    except ValueError:
        return (position_str, None)


def _parse_score(score_str: Optional[str]) -> tuple[Optional[str], Optional[int]]:
    """
    Parse score string to (string, strokes) tuple.

    Args:
        score_str: Score string (e.g., "-12", "E", "+3")

    Returns:
        Tuple of (score_string, total_strokes or None)
    """
    if not score_str:
        return (None, None)

    score_str = str(score_str).strip()

    # For stroke count, we'd need round scores
    # Just return the score string for now
    return (score_str, None)


def sync_results_from_leaderboard(tournament_id: str) -> Dict[str, Any]:
    """
    Sync tournament results from leaderboard (for in-progress or completed tournaments).

    This syncs position and scoring data but NOT earnings (leaderboard doesn't include earnings).
    For earnings, use sync_results_with_earnings() after tournament is completed.

    Args:
        tournament_id: Tournament ID (e.g., "R2024016")

    Returns:
        Dictionary with sync results
    """
    operation = f"results_sync_leaderboard_{tournament_id}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Syncing results from leaderboard for tournament {tournament_id}")

        # Fetch leaderboard
        with pga_client() as client:
            leaderboard = client.get_leaderboard(tournament_id)

        if not leaderboard:
            logger.warning(f"No leaderboard data found for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "results_synced": 0,
                "message": "No leaderboard data found"
            }

        # Extract player results
        results_to_upsert = []
        players = leaderboard.get("players", [])

        for player_row in players:
            # Handle union type - only process PlayerRowV3
            if not player_row.get("player"):
                continue

            player = player_row["player"]
            scoring_data = player_row.get("scoringData", {})

            player_id = player.get("id")
            if not player_id:
                continue

            # Parse position
            position_str, position_numeric = _parse_position(scoring_data.get("position"))

            # Parse rounds (convert array to JSON)
            rounds = scoring_data.get("rounds", [])
            rounds_json = json.dumps(rounds) if rounds else None

            # Determine status based on playerState
            player_state = scoring_data.get("playerState", "ACTIVE")
            status = player_state.upper()

            # Check if official
            is_official = leaderboard.get("tournamentStatus") in ("OFFICIAL", "COMPLETED")

            results_to_upsert.append({
                "tournament_id": tournament_id,
                "player_id": player_id,
                "position": position_str,
                "position_numeric": position_numeric,
                "total_score": scoring_data.get("total"),
                "total_strokes": scoring_data.get("totalStrokesSort"),
                "rounds": rounds_json,
                "earnings": Decimal("0"),  # Leaderboard doesn't have earnings
                "fedex_points": None,  # Not in basic leaderboard
                "status": status,
                "is_official": is_official
            })

        if not results_to_upsert:
            logger.info(f"No results to sync for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "results_synced": 0,
                "message": "No results to sync"
            }

        # Upsert to database
        records_affected = upsert_records(
            table="tournament_results",
            records=results_to_upsert,
            conflict_columns=["tournament_id", "player_id"],
            update_columns=["position", "position_numeric", "total_score",
                           "total_strokes", "rounds", "status", "is_official"]
        )

        logger.info(f"Successfully synced {records_affected} results for tournament {tournament_id}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "results_synced": records_affected,
            "tournament_id": tournament_id,
            "note": "Earnings not included - use sync_results_with_earnings() for completed tournaments"
        }

    except Exception as e:
        error_msg = f"Error syncing results from leaderboard: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "results_synced": 0,
            "error": error_msg
        }


def sync_results_with_earnings(tournament_id: str, year: int = None) -> Dict[str, Any]:
    """
    Sync tournament results WITH earnings for a completed tournament.

    This queries each player's season results to get earnings for the tournament.
    Only use this for COMPLETED tournaments.

    Args:
        tournament_id: Tournament ID (e.g., "R2024016")
        year: Season year (defaults to current year)

    Returns:
        Dictionary with sync results
    """
    if year is None:
        year = datetime.now().year

    operation = f"results_sync_earnings_{tournament_id}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Syncing earnings for tournament {tournament_id}")

        # First, get all players who have results for this tournament (from tournament_results table)
        query = """
            SELECT DISTINCT player_id
            FROM tournament_results
            WHERE tournament_id = %s
        """
        player_records = execute_dict_query(query, (tournament_id,))

        if not player_records:
            logger.warning(f"No existing results found for tournament {tournament_id}. Run sync_results_from_leaderboard() first.")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "earnings_updated": 0,
                "message": "No existing results found"
            }

        # Query each player's season to get earnings for this tournament
        earnings_updates = []

        with pga_client() as client:
            for player_record in player_records:
                player_id = player_record["player_id"]

                try:
                    # Get player's season results
                    season_data = client.get_player_season(
                        player_id=player_id,
                        year=year,
                        tour_code="R"
                    )

                    # Find the tournament in their season results
                    tournaments = season_data.get("tournaments", [])
                    for tournament in tournaments:
                        if tournament.get("tournamentId") == tournament_id:
                            money = _parse_money(tournament.get("money"))
                            fedex_points = tournament.get("points")

                            earnings_updates.append({
                                "tournament_id": tournament_id,
                                "player_id": player_id,
                                "earnings": money,
                                "fedex_points": fedex_points,
                                "position": tournament.get("finishPosition"),
                                "total_score": tournament.get("toPar")
                            })
                            break

                except Exception as e:
                    logger.warning(f"Error fetching season data for player {player_id}: {e}")
                    continue

        if not earnings_updates:
            logger.warning(f"No earnings data found for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "earnings_updated": 0,
                "message": "No earnings data found"
            }

        # Update earnings in database
        records_affected = upsert_records(
            table="tournament_results",
            records=earnings_updates,
            conflict_columns=["tournament_id", "player_id"],
            update_columns=["earnings", "fedex_points", "position", "total_score"]
        )

        logger.info(f"Successfully updated earnings for {records_affected} players in tournament {tournament_id}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "earnings_updated": records_affected,
            "tournament_id": tournament_id
        }

    except Exception as e:
        error_msg = f"Error syncing earnings: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "earnings_updated": 0,
            "error": error_msg
        }


def sync_results(tournament_id: str, include_earnings: bool = True, year: int = None) -> Dict[str, Any]:
    """
    Complete results sync for a tournament.

    Args:
        tournament_id: Tournament ID
        include_earnings: Whether to fetch earnings (for completed tournaments)
        year: Season year

    Returns:
        Dictionary with sync results
    """
    # First sync from leaderboard (position, scores)
    result1 = sync_results_from_leaderboard(tournament_id)

    if not result1["success"]:
        return result1

    # Then sync earnings if requested
    if include_earnings:
        result2 = sync_results_with_earnings(tournament_id, year)
        return {
            "success": result1["success"] and result2["success"],
            "results_synced": result1["results_synced"],
            "earnings_updated": result2.get("earnings_updated", 0),
            "tournament_id": tournament_id
        }

    return result1


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Example: Sync results for The Sentry 2024
    tournament_id = "R2024016"
    result = sync_results(tournament_id, include_earnings=True, year=2024)

    print(f"\nSync Results:")
    print(f"  Tournament: {result.get('tournament_id')}")
    print(f"  Results Synced: {result.get('results_synced')}")
    print(f"  Earnings Updated: {result.get('earnings_updated')}")
    print(f"  Success: {result['success']}")
