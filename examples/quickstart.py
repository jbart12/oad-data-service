#!/usr/bin/env python3
"""
Quick Start Guide - PGA Data Sync Service

This script demonstrates the main sync operations.
Run this to populate your database for the first time.
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.sync.players import sync_all_tours
from services.sync.schedule import sync_schedule_multi_year
from services.sync.leaderboard import sync_tournament_field
from services.sync.results import sync_results
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def quickstart():
    """Run a complete initial sync."""

    print("=" * 70)
    print("PGA DATA SYNC SERVICE - QUICK START")
    print("=" * 70)
    print()

    # Step 1: Sync Players
    print("STEP 1: Syncing Players")
    print("-" * 70)
    result = sync_all_tours(active_only=True)
    print(f"✓ Synced {result['total_players_synced']} players across all tours")
    print()

    # Step 2: Sync Schedule
    print("STEP 2: Syncing Tournament Schedule")
    print("-" * 70)
    current_year = datetime.now().year
    result = sync_schedule_multi_year(years=[current_year, current_year + 1])
    print(f"✓ Synced {result['total_tournaments_synced']} tournaments")
    print()

    # Step 3: Example - Sync a specific tournament
    print("STEP 3: Example - Sync Tournament Field & Results")
    print("-" * 70)
    tournament_id = "R2024016"  # The Sentry 2024

    # Sync field
    field_result = sync_tournament_field(tournament_id)
    print(f"✓ Field: {field_result['field_entries_synced']} players")

    # Sync results with earnings
    results_result = sync_results(tournament_id, include_earnings=True, year=2024)
    print(f"✓ Results: {results_result.get('results_synced', 0)} players")
    print(f"✓ Earnings: {results_result.get('earnings_updated', 0)} players")
    print()

    print("=" * 70)
    print("QUICK START COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Set up cron jobs (see jobs/README.md)")
    print("2. Monitor sync logs (see logs/ directory)")
    print("3. Query the database to verify data")
    print()


def show_database_queries():
    """Show example database queries to verify data."""

    print("\nExample Database Queries:")
    print("-" * 70)

    queries = [
        ("Count Players", "SELECT COUNT(*) FROM players;"),
        ("Count Tournaments", "SELECT COUNT(*) FROM tournaments;"),
        ("Recent Tournaments", """
            SELECT name, start_date, status
            FROM tournaments
            ORDER BY start_date DESC
            LIMIT 5;
        """),
        ("Top Earners", """
            SELECT p.display_name, SUM(tr.earnings) as total_earnings
            FROM tournament_results tr
            JOIN players p ON tr.player_id = p.id
            GROUP BY p.id, p.display_name
            ORDER BY total_earnings DESC
            LIMIT 10;
        """),
        ("Sync Log", """
            SELECT operation, status, records_affected, synced_at
            FROM sync_log
            ORDER BY synced_at DESC
            LIMIT 10;
        """)
    ]

    for title, query in queries:
        print(f"\n{title}:")
        print(query)


if __name__ == "__main__":
    try:
        quickstart()
        show_database_queries()
    except Exception as e:
        logger.error(f"Error during quickstart: {e}", exc_info=True)
        sys.exit(1)
