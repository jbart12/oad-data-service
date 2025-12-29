#!/usr/bin/env python3
"""
Daily Sync Job

Schedule: Mon-Wed at 6:00 AM ET
Purpose: Update tournament fields for upcoming events

Operations:
1. Sync tournament fields for upcoming/in-progress tournaments
2. Update tournament status
3. Light cleanup operations
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.sync.leaderboard import sync_tournament_field
from database import log_sync, execute_dict_query, execute_query, DatabasePool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(project_root / "logs" / f"daily_sync_{datetime.now():%Y%m%d}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def get_upcoming_tournaments(days_ahead: int = 14):
    """
    Get upcoming tournaments within the next N days.

    Args:
        days_ahead: Number of days to look ahead

    Returns:
        List of tournament dictionaries
    """
    query = """
        SELECT id, name, start_date, status
        FROM tournaments
        WHERE start_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '%s days'
        AND status IN ('UPCOMING', 'IN_PROGRESS')
        ORDER BY start_date ASC
    """

    return execute_dict_query(query, (days_ahead,))


def sync_upcoming_tournament_fields():
    """
    Sync fields for upcoming tournaments.

    Returns:
        Dictionary with sync results
    """
    logger.info("Syncing fields for upcoming tournaments...")

    tournaments = get_upcoming_tournaments(days_ahead=14)

    results = {
        "tournaments_processed": 0,
        "total_field_entries": 0,
        "errors": []
    }

    if not tournaments:
        logger.info("No upcoming tournaments found")
        return results

    logger.info(f"Found {len(tournaments)} upcoming tournaments")

    for tournament in tournaments:
        tournament_id = tournament["id"]
        tournament_name = tournament["name"]
        start_date = tournament["start_date"]

        logger.info(f"Processing {tournament_name} ({start_date})...")

        try:
            result = sync_tournament_field(tournament_id)

            if result["success"]:
                results["tournaments_processed"] += 1
                results["total_field_entries"] += result["field_entries_synced"]
                logger.info(f"  ✓ {result['field_entries_synced']} players in field")
            else:
                error = f"{tournament_name}: {result.get('error', 'Unknown error')}"
                results["errors"].append(error)
                logger.error(f"  ✗ {error}")

        except Exception as e:
            error = f"{tournament_name}: {str(e)}"
            results["errors"].append(error)
            logger.error(f"  ✗ {error}", exc_info=True)

    return results


def update_tournament_statuses():
    """
    Update tournament statuses based on dates.

    Returns:
        Number of tournaments updated
    """
    logger.info("Updating tournament statuses...")

    # Mark tournaments as IN_PROGRESS if they've started
    query_start = """
        UPDATE tournaments
        SET status = 'IN_PROGRESS'
        WHERE status = 'UPCOMING'
        AND start_date <= CURRENT_DATE
        AND end_date >= CURRENT_DATE
    """

    # Mark tournaments as COMPLETED if they've ended (but only if not already marked)
    query_end = """
        UPDATE tournaments
        SET status = 'COMPLETED'
        WHERE status IN ('UPCOMING', 'IN_PROGRESS')
        AND end_date < CURRENT_DATE
    """

    started = execute_query(query_start, fetch=False)
    ended = execute_query(query_end, fetch=False)

    logger.info(f"  Marked {started} tournaments as IN_PROGRESS")
    logger.info(f"  Marked {ended} tournaments as COMPLETED")

    return started + ended


def cleanup_old_snapshots(days_to_keep: int = 30):
    """
    Clean up old leaderboard snapshots.

    Args:
        days_to_keep: Number of days of snapshots to retain

    Returns:
        Number of snapshots deleted
    """
    logger.info(f"Cleaning up snapshots older than {days_to_keep} days...")

    query = """
        DELETE FROM leaderboard_snapshots
        WHERE snapshot_time < NOW() - INTERVAL '%s days'
    """

    execute_query(query, (days_to_keep,), fetch=False)
    logger.info("  ✓ Old snapshots cleaned up")

    return 0  # Can't get count from DELETE without RETURNING


def run_daily_sync():
    """
    Execute daily sync operations.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("DAILY SYNC STARTING")
    logger.info(f"Start Time: {start_time}")
    logger.info(f"Day: {start_time.strftime('%A, %B %d, %Y')}")
    logger.info("=" * 60)

    operation = f"daily_sync_{start_time:%Y%m%d_%H%M%S}"
    log_id = log_sync(operation, "in_progress")

    overall_success = True
    summary = {
        "field_sync": {},
        "status_updates": 0,
        "start_time": start_time
    }

    try:
        # Step 1: Sync Tournament Fields
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: Syncing Tournament Fields")
        logger.info("=" * 60)

        field_result = sync_upcoming_tournament_fields()
        summary["field_sync"] = field_result

        if field_result["errors"]:
            logger.warning(f"⚠ Some fields had errors: {len(field_result['errors'])}")
            for error in field_result["errors"]:
                logger.warning(f"  - {error}")

        logger.info(f"✓ Tournaments processed: {field_result['tournaments_processed']}")
        logger.info(f"✓ Field entries synced: {field_result['total_field_entries']}")

        # Step 2: Update Tournament Statuses
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Updating Tournament Statuses")
        logger.info("=" * 60)

        status_updates = update_tournament_statuses()
        summary["status_updates"] = status_updates

        logger.info(f"✓ Tournament statuses updated: {status_updates}")

        # Step 3: Cleanup (only on Mondays)
        if start_time.weekday() == 0:  # Monday
            logger.info("\n" + "=" * 60)
            logger.info("STEP 3: Cleanup (Monday only)")
            logger.info("=" * 60)

            cleanup_old_snapshots(days_to_keep=30)
            logger.info("✓ Cleanup completed")

        # Final Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("\n" + "=" * 60)
        logger.info("DAILY SYNC COMPLETED")
        logger.info("=" * 60)
        logger.info(f"End Time: {end_time}")
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Status: {'SUCCESS' if overall_success else 'PARTIAL FAILURE'}")
        logger.info("\nSummary:")
        logger.info(f"  Tournaments Processed: {summary['field_sync']['tournaments_processed']}")
        logger.info(f"  Field Entries Synced: {summary['field_sync']['total_field_entries']}")
        logger.info(f"  Status Updates: {summary['status_updates']}")

        # Log to database
        total_records = (
            summary['field_sync']['total_field_entries'] +
            summary['status_updates']
        )

        log_sync(
            operation,
            "success" if overall_success else "error",
            records_affected=total_records,
            error_message=None if overall_success else "Some operations failed"
        )

        return 0 if overall_success else 1

    except Exception as e:
        logger.error(f"Fatal error in daily sync: {e}", exc_info=True)
        log_sync(operation, "error", error_message=str(e))
        return 1

    finally:
        # Close database pool
        DatabasePool.close_all()


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Run sync
    exit_code = run_daily_sync()
    sys.exit(exit_code)
