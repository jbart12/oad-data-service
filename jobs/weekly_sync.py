#!/usr/bin/env python3
"""
Weekly Full Sync Job

Schedule: Sundays at 11:00 PM ET
Purpose: Complete data refresh

Operations:
1. Sync all players (PGA, Champions, Korn Ferry tours)
2. Sync tournament schedule (current + next year)
3. Sync completed tournament results with earnings
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.sync import sync_players, sync_schedule, sync_results
from services.sync.players import sync_all_tours
from services.sync.schedule import sync_schedule_multi_year
from database import log_sync, execute_dict_query, DatabasePool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(project_root / "logs" / f"weekly_sync_{datetime.now():%Y%m%d}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def sync_completed_tournaments():
    """
    Sync results for all completed tournaments that need earnings data.

    Returns:
        Dictionary with sync results
    """
    logger.info("Syncing completed tournaments...")

    # Find completed tournaments without earnings data
    query = """
        SELECT DISTINCT t.id, t.name, t.season_year
        FROM tournaments t
        WHERE t.status = 'COMPLETED'
        AND NOT EXISTS (
            SELECT 1 FROM tournament_results tr
            WHERE tr.tournament_id = t.id
            AND tr.earnings > 0
        )
        ORDER BY t.season_year DESC, t.start_date DESC
        LIMIT 20
    """

    tournaments = execute_dict_query(query)

    results = {
        "tournaments_processed": 0,
        "results_synced": 0,
        "earnings_updated": 0,
        "errors": []
    }

    for tournament in tournaments:
        tournament_id = tournament["id"]
        tournament_name = tournament["name"]
        year = tournament["season_year"]

        logger.info(f"Processing {tournament_name} ({tournament_id})...")

        try:
            result = sync_results(tournament_id, include_earnings=True, year=year)

            if result["success"]:
                results["tournaments_processed"] += 1
                results["results_synced"] += result.get("results_synced", 0)
                results["earnings_updated"] += result.get("earnings_updated", 0)
            else:
                error = f"{tournament_name}: {result.get('error', 'Unknown error')}"
                results["errors"].append(error)
                logger.error(error)

        except Exception as e:
            error = f"{tournament_name}: {str(e)}"
            results["errors"].append(error)
            logger.error(error, exc_info=True)

    return results


def run_weekly_sync():
    """
    Execute complete weekly sync.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("WEEKLY SYNC STARTING")
    logger.info(f"Start Time: {start_time}")
    logger.info("=" * 60)

    operation = f"weekly_sync_{start_time:%Y%m%d_%H%M%S}"
    log_id = log_sync(operation, "in_progress")

    overall_success = True
    summary = {
        "players": {},
        "schedule": {},
        "tournaments": {},
        "start_time": start_time
    }

    try:
        # Step 1: Sync Players
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: Syncing Players")
        logger.info("=" * 60)

        players_result = sync_all_tours(active_only=True)
        summary["players"] = players_result

        if players_result["success"]:
            logger.info(f"✓ Players synced: {players_result['total_players_synced']}")
        else:
            logger.error(f"✗ Player sync failed: {players_result.get('errors')}")
            overall_success = False

        # Step 2: Sync Schedule
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Syncing Tournament Schedule")
        logger.info("=" * 60)

        current_year = datetime.now().year
        schedule_result = sync_schedule_multi_year(
            tour_code="R",
            years=[current_year, current_year + 1]
        )
        summary["schedule"] = schedule_result

        if schedule_result["success"]:
            logger.info(f"✓ Tournaments synced: {schedule_result['total_tournaments_synced']}")
        else:
            logger.error(f"✗ Schedule sync failed: {schedule_result.get('errors')}")
            overall_success = False

        # Step 3: Sync Completed Tournament Results
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: Syncing Completed Tournament Results")
        logger.info("=" * 60)

        tournaments_result = sync_completed_tournaments()
        summary["tournaments"] = tournaments_result

        if tournaments_result["errors"]:
            logger.warning(f"⚠ Some tournaments had errors: {len(tournaments_result['errors'])}")
            for error in tournaments_result["errors"]:
                logger.warning(f"  - {error}")

        logger.info(f"✓ Tournaments processed: {tournaments_result['tournaments_processed']}")
        logger.info(f"✓ Results synced: {tournaments_result['results_synced']}")
        logger.info(f"✓ Earnings updated: {tournaments_result['earnings_updated']}")

        # Final Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("\n" + "=" * 60)
        logger.info("WEEKLY SYNC COMPLETED")
        logger.info("=" * 60)
        logger.info(f"End Time: {end_time}")
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Status: {'SUCCESS' if overall_success else 'PARTIAL FAILURE'}")
        logger.info("\nSummary:")
        logger.info(f"  Players Synced: {summary['players'].get('total_players_synced', 0)}")
        logger.info(f"  Tournaments Synced: {summary['schedule'].get('total_tournaments_synced', 0)}")
        logger.info(f"  Results Synced: {summary['tournaments'].get('results_synced', 0)}")
        logger.info(f"  Earnings Updated: {summary['tournaments'].get('earnings_updated', 0)}")

        # Log to database
        total_records = (
            summary['players'].get('total_players_synced', 0) +
            summary['schedule'].get('total_tournaments_synced', 0) +
            summary['tournaments'].get('results_synced', 0)
        )

        log_sync(
            operation,
            "success" if overall_success else "error",
            records_affected=total_records,
            error_message=None if overall_success else "Some operations failed"
        )

        return 0 if overall_success else 1

    except Exception as e:
        logger.error(f"Fatal error in weekly sync: {e}", exc_info=True)
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
    exit_code = run_weekly_sync()
    sys.exit(exit_code)
