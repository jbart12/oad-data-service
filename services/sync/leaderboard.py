"""
Live leaderboard synchronization.

Takes snapshots of tournament leaderboards for real-time scoring during events.
Used for live polling Thu-Sun during tournament weeks.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from decimal import Decimal

from ..pga_client import pga_client
from database import execute_query, log_sync, get_db_cursor

logger = logging.getLogger(__name__)


def sync_leaderboard(tournament_id: str) -> Dict[str, Any]:
    """
    Take a snapshot of the current leaderboard for a tournament.

    This inserts a new snapshot record for each player on the leaderboard.
    Used for tracking live scoring progression during tournaments.

    Args:
        tournament_id: Tournament ID (e.g., "R2024016")

    Returns:
        Dictionary with sync results:
            - success: bool
            - snapshots_created: int
            - snapshot_time: datetime
            - tournament_status: str
            - error: Optional error message
    """
    operation = f"leaderboard_sync_{tournament_id}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Taking leaderboard snapshot for tournament {tournament_id}")

        # Fetch current leaderboard
        with pga_client() as client:
            leaderboard = client.get_leaderboard(tournament_id)

        if not leaderboard:
            logger.warning(f"No leaderboard data found for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "snapshots_created": 0,
                "message": "No leaderboard data found"
            }

        tournament_status = leaderboard.get("tournamentStatus", "UNKNOWN")
        snapshot_time = datetime.now(timezone.utc)

        # Extract player snapshots
        snapshots = []
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

            snapshots.append({
                "tournament_id": tournament_id,
                "player_id": player_id,
                "position": scoring_data.get("position"),
                "total": scoring_data.get("total"),
                "today": scoring_data.get("score"),  # Today's score
                "thru": scoring_data.get("thru"),
                "current_round": scoring_data.get("currentRound"),
                "player_state": scoring_data.get("playerState"),
                "projected_earnings": None,  # Not available in basic leaderboard
                "snapshot_time": snapshot_time
            })

        if not snapshots:
            logger.info(f"No players found on leaderboard for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "snapshots_created": 0,
                "tournament_status": tournament_status,
                "message": "No players found"
            }

        # Insert snapshots into database (batch insert)
        columns = list(snapshots[0].keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        insert_query = f"""
            INSERT INTO leaderboard_snapshots ({columns_str})
            VALUES ({placeholders})
        """

        with get_db_cursor() as cur:
            from psycopg2.extras import execute_batch
            values = [[snapshot.get(col) for col in columns] for snapshot in snapshots]
            execute_batch(cur, insert_query, values)
            records_affected = cur.rowcount

        logger.info(f"Created {records_affected} leaderboard snapshots for tournament {tournament_id}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "snapshots_created": records_affected,
            "snapshot_time": snapshot_time,
            "tournament_id": tournament_id,
            "tournament_status": tournament_status
        }

    except Exception as e:
        error_msg = f"Error syncing leaderboard: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "snapshots_created": 0,
            "error": error_msg
        }


def sync_tournament_field(tournament_id: str) -> Dict[str, Any]:
    """
    Sync tournament field (players in the tournament).

    This populates the tournament_fields table with the list of players
    competing in a tournament.

    Args:
        tournament_id: Tournament ID

    Returns:
        Dictionary with sync results
    """
    operation = f"field_sync_{tournament_id}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Syncing field for tournament {tournament_id}")

        # Fetch tournament field
        with pga_client() as client:
            field_data = client.get_tournament_field(tournament_id)

        if not field_data:
            logger.warning(f"No field data found for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "field_entries_synced": 0,
                "message": "No field data found"
            }

        players = field_data.get("players", [])

        if not players:
            logger.warning(f"No players in field for tournament {tournament_id}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "field_entries_synced": 0,
                "message": "No players in field"
            }

        # Prepare field entries
        field_entries = []
        for player in players:
            player_id = player.get("id")
            if not player_id:
                continue

            field_entries.append({
                "tournament_id": tournament_id,
                "player_id": player_id,
                "status": "ACTIVE"
            })

        # Insert field entries (ON CONFLICT DO NOTHING since we just need the roster)
        if field_entries:
            from database import upsert_records
            records_affected = upsert_records(
                table="tournament_fields",
                records=field_entries,
                conflict_columns=["tournament_id", "player_id"],
                update_columns=["status"]
            )
        else:
            records_affected = 0

        logger.info(f"Synced {records_affected} field entries for tournament {tournament_id}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "field_entries_synced": records_affected,
            "tournament_id": tournament_id
        }

    except Exception as e:
        error_msg = f"Error syncing tournament field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "field_entries_synced": 0,
            "error": error_msg
        }


def get_latest_snapshot(tournament_id: str, player_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the latest leaderboard snapshot for a tournament or player.

    Args:
        tournament_id: Tournament ID
        player_id: Optional player ID to filter by

    Returns:
        Latest snapshot data or empty dict
    """
    from database import execute_dict_query

    if player_id:
        query = """
            SELECT *
            FROM leaderboard_snapshots
            WHERE tournament_id = %s AND player_id = %s
            ORDER BY snapshot_time DESC
            LIMIT 1
        """
        params = (tournament_id, player_id)
    else:
        query = """
            SELECT *
            FROM leaderboard_snapshots
            WHERE tournament_id = %s
            ORDER BY snapshot_time DESC
            LIMIT 100
        """
        params = (tournament_id,)

    results = execute_dict_query(query, params)

    if player_id:
        return results[0] if results else {}
    else:
        return {"snapshots": results, "count": len(results)}


def cleanup_old_snapshots(days_to_keep: int = 7) -> Dict[str, Any]:
    """
    Clean up old leaderboard snapshots.

    Args:
        days_to_keep: Number of days of snapshots to retain

    Returns:
        Dictionary with cleanup results
    """
    try:
        logger.info(f"Cleaning up snapshots older than {days_to_keep} days")

        query = """
            DELETE FROM leaderboard_snapshots
            WHERE snapshot_time < NOW() - INTERVAL '%s days'
        """

        result = execute_query(query, (days_to_keep,), fetch=False)

        logger.info(f"Cleaned up old snapshots")

        return {
            "success": True,
            "message": f"Cleaned up snapshots older than {days_to_keep} days"
        }

    except Exception as e:
        error_msg = f"Error cleaning up snapshots: {str(e)}"
        logger.error(error_msg, exc_info=True)

        return {
            "success": False,
            "error": error_msg
        }


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Example: Take snapshot of The Sentry 2024
    tournament_id = "R2024016"

    # Sync field first
    field_result = sync_tournament_field(tournament_id)
    print(f"\nField Sync Results:")
    print(f"  Field Entries Synced: {field_result['field_entries_synced']}")
    print(f"  Success: {field_result['success']}")

    # Take leaderboard snapshot
    snapshot_result = sync_leaderboard(tournament_id)
    print(f"\nLeaderboard Snapshot Results:")
    print(f"  Snapshots Created: {snapshot_result['snapshots_created']}")
    print(f"  Tournament Status: {snapshot_result.get('tournament_status')}")
    print(f"  Success: {snapshot_result['success']}")
