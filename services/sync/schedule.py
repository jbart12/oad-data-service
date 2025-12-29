"""
Tournament schedule synchronization.

Syncs tournament schedule from PGA Tour API to the database.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from ..pga_client import pga_client
from database import upsert_records, log_sync, execute_query

logger = logging.getLogger(__name__)


def _parse_purse(purse_str: Optional[str]) -> Optional[Decimal]:
    """
    Parse purse string to Decimal.

    Args:
        purse_str: Purse string (e.g., "$20,000,000")

    Returns:
        Decimal value or None
    """
    if not purse_str:
        return None

    try:
        # Remove $ and commas
        cleaned = purse_str.replace("$", "").replace(",", "").strip()
        return Decimal(cleaned) if cleaned else None
    except (ValueError, InvalidOperation):
        logger.warning(f"Could not parse purse: {purse_str}")
        return None


def _parse_timestamp(timestamp: Optional[int]) -> Optional[datetime]:
    """
    Parse AWSTimestamp to datetime.

    Args:
        timestamp: AWS timestamp (seconds since epoch)

    Returns:
        datetime object or None
    """
    if not timestamp:
        return None

    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
    except (ValueError, TypeError, OSError):
        logger.warning(f"Could not parse timestamp: {timestamp}")
        return None


def _map_tournament_status(api_status: Optional[str]) -> str:
    """
    Map API tournament status to database status.

    Args:
        api_status: Status from API (e.g., "IN_PROGRESS", "COMPLETED", "UPCOMING")

    Returns:
        Database status value
    """
    if not api_status:
        return "UPCOMING"

    status_map = {
        "SCHEDULED": "UPCOMING",
        "IN_PROGRESS": "IN_PROGRESS",
        "OFFICIAL": "COMPLETED",
        "COMPLETED": "COMPLETED",
        "CANCELLED": "CANCELLED",
        "CANCELED": "CANCELLED",
        "POSTPONED": "UPCOMING"
    }

    return status_map.get(api_status.upper(), "UPCOMING")


def sync_schedule(tour_code: str = "R", year: str = None) -> Dict[str, Any]:
    """
    Sync tournament schedule from PGA Tour API to database.

    Args:
        tour_code: Tour code (R=PGA Tour, H=Champions, M=Korn Ferry)
        year: Season year (defaults to current year)

    Returns:
        Dictionary with sync results:
            - success: bool
            - tournaments_synced: int
            - error: Optional error message
    """
    if year is None:
        year = str(datetime.now().year)

    operation = f"schedule_sync_{tour_code}_{year}"
    log_id = log_sync(operation, "in_progress")

    try:
        logger.info(f"Starting schedule sync for tour {tour_code}, year {year}")

        # Fetch schedule from API with full tournament details
        with pga_client() as client:
            result = client.query(
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
                                startDate
                                date
                                city
                                state
                                country
                                courseName
                                purse
                                tournamentStatus
                                sequenceNumber
                            }
                        }
                        upcoming {
                            month
                            year
                            tournaments {
                                id
                                tournamentName
                                startDate
                                date
                                city
                                state
                                country
                                courseName
                                purse
                                tournamentStatus
                                sequenceNumber
                            }
                        }
                    }
                }
                """,
                {"tourCode": tour_code, "year": year}
            )

        schedule_data = result.get("data", {}).get("schedule", {})

        if not schedule_data:
            logger.warning(f"No schedule data found for tour {tour_code}, year {year}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "tournaments_synced": 0,
                "message": "No schedule data found"
            }

        # Extract tournaments from both completed and upcoming
        tournaments_to_upsert = []

        for section in [schedule_data.get("completed", []), schedule_data.get("upcoming", [])]:
            for month_group in section:
                for tournament in month_group.get("tournaments", []):
                    if not tournament.get("id"):
                        logger.warning(f"Skipping tournament without ID: {tournament}")
                        continue

                    # Parse start date
                    start_date = _parse_timestamp(tournament.get("startDate"))

                    # Estimate end date (tournaments typically last 4 days, Thu-Sun)
                    end_date = None
                    if start_date:
                        from datetime import timedelta
                        end_date = start_date + timedelta(days=3)

                    # Parse purse
                    purse = _parse_purse(tournament.get("purse"))

                    # Map status
                    status = _map_tournament_status(tournament.get("tournamentStatus"))

                    tournaments_to_upsert.append({
                        "id": tournament["id"],
                        "name": tournament.get("tournamentName", ""),
                        "season_year": int(year),
                        "tour_code": tour_code,
                        "start_date": start_date.date() if start_date else None,
                        "end_date": end_date.date() if end_date else None,
                        "course_name": tournament.get("courseName"),
                        "city": tournament.get("city"),
                        "state": tournament.get("state"),
                        "country": tournament.get("country"),
                        "purse": purse,
                        "status": status
                    })

        if not tournaments_to_upsert:
            logger.info(f"No tournaments to sync for tour {tour_code}, year {year}")
            log_sync(operation, "success", records_affected=0)
            return {
                "success": True,
                "tournaments_synced": 0,
                "message": "No tournaments to sync"
            }

        # Upsert to database
        records_affected = upsert_records(
            table="tournaments",
            records=tournaments_to_upsert,
            conflict_columns=["id"],
            update_columns=["name", "start_date", "end_date", "course_name",
                           "city", "state", "country", "purse", "status"]
        )

        logger.info(f"Successfully synced {records_affected} tournaments for tour {tour_code}, year {year}")
        log_sync(operation, "success", records_affected=records_affected)

        return {
            "success": True,
            "tournaments_synced": records_affected,
            "tour_code": tour_code,
            "year": year
        }

    except Exception as e:
        error_msg = f"Error syncing schedule: {str(e)}"
        logger.error(error_msg, exc_info=True)
        log_sync(operation, "error", error_message=error_msg)

        return {
            "success": False,
            "tournaments_synced": 0,
            "error": error_msg
        }


def sync_schedule_multi_year(tour_code: str = "R", years: List[int] = None) -> Dict[str, Any]:
    """
    Sync tournament schedule for multiple years.

    Args:
        tour_code: Tour code
        years: List of years to sync (defaults to current year)

    Returns:
        Dictionary with aggregated sync results
    """
    if years is None:
        years = [datetime.now().year]

    results = {}
    total_synced = 0
    errors = []

    for year in years:
        logger.info(f"Syncing schedule for year {year}...")
        result = sync_schedule(tour_code=tour_code, year=str(year))

        results[year] = result
        if result["success"]:
            total_synced += result["tournaments_synced"]
        else:
            errors.append(f"Year {year}: {result.get('error', 'Unknown error')}")

    return {
        "success": len(errors) == 0,
        "total_tournaments_synced": total_synced,
        "results_by_year": results,
        "errors": errors if errors else None
    }


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Sync current and next year
    current_year = datetime.now().year
    result = sync_schedule_multi_year(years=[current_year, current_year + 1])

    print(f"\nSync Results:")
    print(f"  Total Tournaments Synced: {result['total_tournaments_synced']}")
    print(f"  Success: {result['success']}")
    if result.get('errors'):
        print(f"  Errors: {result['errors']}")
