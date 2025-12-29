"""
Player data synchronization.

Syncs player directory from PGA Tour API to the database.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..pga_client import pga_client
from database import upsert_records, log_sync

logger = logging.getLogger(__name__)


def sync_players(tour_code: str = "R", active_only: bool = True) -> Dict[str, Any]:
    """
    Sync players from PGA Tour API to database.

    Args:
        tour_code: Tour code (R=PGA Tour, H=Champions, M=Korn Ferry)
        active_only: Whether to sync only active players

    Returns:
        Dictionary with sync results:
            - success: bool
            - players_synced: int
            - error: Optional error message
    """
    operation = f"players_sync_{tour_code}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Starting players sync for tour {tour_code} (active_only={active_only})")

        # Fetch players from API
        with pga_client() as client:
            players_data = client.get_players(tour_code=tour_code, active=active_only)

        if not players_data:
            logger.warning(f"No players found for tour {tour_code}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "players_synced": 0,
                "message": "No players found"
            }

        # Transform API data to database format
        players_to_upsert = []
        for player in players_data:
            # Skip players without ID
            if not player.get("id"):
                logger.warning(f"Skipping player without ID: {player}")
                continue

            players_to_upsert.append({
                "id": player["id"],
                "first_name": player.get("firstName", ""),
                "last_name": player.get("lastName", ""),
                "display_name": player.get("displayName", ""),
                "country": player.get("country"),
                "country_flag": player.get("countryFlag"),
                "headshot_url": player.get("headshot"),
                "is_active": player.get("isActive", True)
            })

        # Upsert to database
        records_affected = upsert_records(
            table="players",
            records=players_to_upsert,
            conflict_columns=["id"],
            update_columns=["first_name", "last_name", "display_name", "country",
                           "country_flag", "headshot_url", "is_active"]
        )

        logger.info(f"Successfully synced {records_affected} players for tour {tour_code}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "players_synced": records_affected,
            "tour_code": tour_code
        }

    except Exception as e:
        error_msg = f"Error syncing players: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "players_synced": 0,
            "error": error_msg
        }


def sync_all_tours(active_only: bool = True) -> Dict[str, Any]:
    """
    Sync players from all major tours.

    Args:
        active_only: Whether to sync only active players

    Returns:
        Dictionary with aggregated sync results
    """
    tours = [
        ("R", "PGA Tour"),
        ("H", "Champions Tour"),
        ("M", "Korn Ferry Tour")
    ]

    results = {}
    total_synced = 0
    errors = []

    for tour_code, tour_name in tours:
        logger.info(f"Syncing {tour_name}...")
        result = sync_players(tour_code=tour_code, active_only=active_only)

        results[tour_code] = result
        if result["success"]:
            total_synced += result["players_synced"]
        else:
            errors.append(f"{tour_name}: {result.get('error', 'Unknown error')}")

    return {
        "success": len(errors) == 0,
        "total_players_synced": total_synced,
        "results_by_tour": results,
        "errors": errors if errors else None
    }


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Sync all tours
    result = sync_all_tours()
    print(f"\nSync Results:")
    print(f"  Total Players Synced: {result['total_players_synced']}")
    print(f"  Success: {result['success']}")
    if result.get('errors'):
        print(f"  Errors: {result['errors']}")
