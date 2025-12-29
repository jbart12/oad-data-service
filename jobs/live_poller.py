#!/usr/bin/env python3
"""
Live Poller Job

Schedule: Thu-Sun during tournament hours (cron runs every 5 min, script decides if it should poll)
Purpose: Real-time leaderboard tracking during active tournaments

Operations:
1. Detect active tournaments
2. Determine tournament phase (ACTIVE, BETWEEN_ROUNDS, NIGHT, etc.)
3. Decide whether to poll based on phase
4. Take leaderboard snapshots
5. Update tournament results
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.sync.leaderboard import sync_leaderboard
from services.sync.results import sync_results_from_leaderboard
from services.scheduler import JitteredScheduler, TournamentPhaseDetector, TournamentPhase
from database import log_sync, execute_dict_query, DatabasePool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(project_root / "logs" / f"live_poller_{datetime.now():%Y%m%d}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def get_active_tournaments() -> List[Dict[str, Any]]:
    """
    Get tournaments that are currently in progress.

    Returns:
        List of active tournament dictionaries
    """
    # Get tournaments that are either:
    # 1. Marked as IN_PROGRESS
    # 2. Within tournament dates (Thu-Sun window)
    query = """
        SELECT id, name, start_date, end_date, status, timezone
        FROM tournaments
        WHERE (
            status = 'IN_PROGRESS'
            OR (
                start_date <= CURRENT_DATE
                AND end_date >= CURRENT_DATE
                AND status != 'COMPLETED'
            )
        )
        ORDER BY start_date ASC
    """

    return execute_dict_query(query)


def get_tournament_status(tournament_id: str) -> str:
    """
    Get current status of a tournament from the API.

    Args:
        tournament_id: Tournament ID

    Returns:
        Tournament status string
    """
    from services import pga_client

    try:
        with pga_client() as client:
            leaderboard = client.get_leaderboard(tournament_id)
            return leaderboard.get("tournamentStatus", "UNKNOWN")
    except Exception as e:
        logger.error(f"Error getting tournament status: {e}")
        return "UNKNOWN"


def poll_tournament(tournament_id: str, tournament_name: str, phase: TournamentPhase) -> Dict[str, Any]:
    """
    Poll a single tournament.

    Args:
        tournament_id: Tournament ID
        tournament_name: Tournament name
        phase: Current tournament phase

    Returns:
        Dictionary with poll results
    """
    logger.info(f"Polling {tournament_name} (phase: {phase.name})...")

    results = {
        "tournament_id": tournament_id,
        "tournament_name": tournament_name,
        "phase": phase.name,
        "snapshot_created": False,
        "results_updated": False,
        "errors": []
    }

    try:
        # Take leaderboard snapshot
        snapshot_result = sync_leaderboard(tournament_id)

        if snapshot_result["success"]:
            results["snapshot_created"] = True
            results["snapshots_count"] = snapshot_result["snapshots_created"]
            results["tournament_status"] = snapshot_result.get("tournament_status")
            logger.info(f"  ✓ Created {snapshot_result['snapshots_created']} snapshots")
        else:
            error = f"Snapshot failed: {snapshot_result.get('error')}"
            results["errors"].append(error)
            logger.error(f"  ✗ {error}")

        # Update tournament results (positions, scores - NOT earnings during live play)
        results_result = sync_results_from_leaderboard(tournament_id)

        if results_result["success"]:
            results["results_updated"] = True
            results["results_count"] = results_result["results_synced"]
            logger.info(f"  ✓ Updated {results_result['results_synced']} results")
        else:
            error = f"Results update failed: {results_result.get('error')}"
            results["errors"].append(error)
            logger.error(f"  ✗ {error}")

    except Exception as e:
        error = f"Poll failed: {str(e)}"
        results["errors"].append(error)
        logger.error(f"  ✗ {error}", exc_info=True)

    return results


def run_live_poller():
    """
    Execute live polling for active tournaments.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    start_time = datetime.now()
    current_hour = start_time.hour

    logger.info("=" * 60)
    logger.info("LIVE POLLER STARTING")
    logger.info(f"Time: {start_time}")
    logger.info(f"Hour: {current_hour} (ET)")
    logger.info("=" * 60)

    operation = f"live_poller_{start_time:%Y%m%d_%H%M%S}"
    log_id = log_sync(operation, "in_progress")

    scheduler = JitteredScheduler(base_rate_limit=2.0)
    overall_success = True

    summary = {
        "active_tournaments": 0,
        "tournaments_polled": 0,
        "total_snapshots": 0,
        "total_results_updated": 0,
        "skipped": [],
        "errors": [],
        "start_time": start_time
    }

    try:
        # Get active tournaments
        tournaments = get_active_tournaments()

        if not tournaments:
            logger.info("No active tournaments found")
            log_sync(operation, "success", records_affected=0)
            return 0

        summary["active_tournaments"] = len(tournaments)
        logger.info(f"Found {len(tournaments)} active tournament(s)")

        # Process each tournament
        for tournament in tournaments:
            tournament_id = tournament["id"]
            tournament_name = tournament["name"]

            logger.info("\n" + "-" * 60)
            logger.info(f"Tournament: {tournament_name}")
            logger.info(f"ID: {tournament_id}")
            logger.info(f"Dates: {tournament['start_date']} to {tournament['end_date']}")

            # Get tournament status from API
            api_status = get_tournament_status(tournament_id)
            logger.info(f"API Status: {api_status}")

            # Determine tournament phase
            phase = TournamentPhaseDetector.get_phase(api_status, current_hour)
            logger.info(f"Phase: {phase.name}")

            # Decide whether to poll based on phase
            if scheduler.should_poll_now(phase):
                logger.info("✓ Polling decision: POLL")

                # Apply rate limiting before polling
                scheduler.rate_limit_wait()

                # Poll the tournament
                poll_result = poll_tournament(tournament_id, tournament_name, phase)

                summary["tournaments_polled"] += 1

                if poll_result["snapshot_created"]:
                    summary["total_snapshots"] += poll_result.get("snapshots_count", 0)

                if poll_result["results_updated"]:
                    summary["total_results_updated"] += poll_result.get("results_count", 0)

                if poll_result["errors"]:
                    summary["errors"].extend(poll_result["errors"])

            else:
                logger.info("✗ Polling decision: SKIP")
                summary["skipped"].append({
                    "tournament": tournament_name,
                    "phase": phase.name,
                    "reason": "Phase-based probability decision"
                })

        # Final Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("\n" + "=" * 60)
        logger.info("LIVE POLLER COMPLETED")
        logger.info("=" * 60)
        logger.info(f"End Time: {end_time}")
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Status: {'SUCCESS' if overall_success else 'PARTIAL FAILURE'}")
        logger.info("\nSummary:")
        logger.info(f"  Active Tournaments: {summary['active_tournaments']}")
        logger.info(f"  Tournaments Polled: {summary['tournaments_polled']}")
        logger.info(f"  Snapshots Created: {summary['total_snapshots']}")
        logger.info(f"  Results Updated: {summary['total_results_updated']}")
        logger.info(f"  Skipped: {len(summary['skipped'])}")

        if summary['skipped']:
            logger.info("\nSkipped Tournaments:")
            for skip in summary['skipped']:
                logger.info(f"  - {skip['tournament']} ({skip['phase']}): {skip['reason']}")

        if summary['errors']:
            logger.warning(f"\nErrors: {len(summary['errors'])}")
            for error in summary['errors']:
                logger.warning(f"  - {error}")

        # Log to database
        total_records = summary['total_snapshots'] + summary['total_results_updated']

        log_sync(
            operation,
            "success" if overall_success else "error",
            records_affected=total_records,
            error_message=None if overall_success else f"{len(summary['errors'])} errors occurred"
        )

        return 0 if overall_success else 1

    except Exception as e:
        logger.error(f"Fatal error in live poller: {e}", exc_info=True)
        log_sync(operation, "error", error_message=str(e))
        return 1

    finally:
        # Close database pool
        DatabasePool.close_all()


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Run poller
    exit_code = run_live_poller()
    sys.exit(exit_code)
