"""
PGA Tour Data Services

A Python client library for the PGA Tour GraphQL API with organic request
patterns designed for the "One and Done" fantasy golf application.

Quick Start:
    from services import pga_client

    with pga_client() as client:
        players = client.get_players()
        leaderboard = client.get_leaderboard("R2024016")

Classes:
    PGAClient: GraphQL client with browser-like headers and rate limiting
    PGAClientError: Exception raised on API failures
    JitteredScheduler: Adds randomness to request timing
    OrganicRequestPattern: Human-like batching and ordering
    TournamentPhase: Enum for tournament phases (ACTIVE, NIGHT, etc.)
    TournamentPhaseDetector: Determines phase from tournament status

Functions:
    pga_client: Context manager for PGAClient
    sleep_with_jitter: Sleep for a randomized duration

See services/README.md for complete documentation.
"""

from .pga_client import PGAClient, PGAClientError, pga_client
from .scheduler import (
    JitteredScheduler,
    OrganicRequestPattern,
    TournamentPhase,
    TournamentPhaseDetector,
    sleep_with_jitter,
)

__all__ = [
    # Client
    "PGAClient",
    "PGAClientError",
    "pga_client",
    # Scheduler
    "JitteredScheduler",
    "OrganicRequestPattern",
    "TournamentPhase",
    "TournamentPhaseDetector",
    "sleep_with_jitter",
]

__version__ = "1.0.0"
