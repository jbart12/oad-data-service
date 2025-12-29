#!/usr/bin/env python3
"""
Randomized Polling Scheduler for PGA Data Service

Implements human-like request patterns with:
- Random jitter on all intervals
- Varied daily sync times
- Organic polling during live events
- Respectful rate limiting
"""

from __future__ import annotations

import random
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, TypeVar, Union

T = TypeVar("T")


class TournamentPhase(Enum):
    """Tournament phases that affect polling frequency."""

    ACTIVE = "active"
    BETWEEN_ROUNDS = "between_rounds"
    WEATHER_DELAY = "weather_delay"
    NIGHT = "night"
    INACTIVE = "inactive"


class JitteredScheduler:
    """
    Scheduler that adds randomness to all timing to avoid
    predictable patterns that look like automated scraping.
    """

    # Base intervals for different tournament phases (seconds)
    PHASE_INTERVALS: dict[TournamentPhase, int] = {
        TournamentPhase.ACTIVE: 180,  # 3 minutes
        TournamentPhase.BETWEEN_ROUNDS: 600,  # 10 minutes
        TournamentPhase.WEATHER_DELAY: 900,  # 15 minutes
        TournamentPhase.NIGHT: 1800,  # 30 minutes
        TournamentPhase.INACTIVE: 3600,  # 1 hour
    }

    # Probability of polling for each phase
    POLL_PROBABILITY: dict[TournamentPhase, float] = {
        TournamentPhase.ACTIVE: 0.95,
        TournamentPhase.BETWEEN_ROUNDS: 0.80,
        TournamentPhase.WEATHER_DELAY: 0.60,
        TournamentPhase.NIGHT: 0.30,
        TournamentPhase.INACTIVE: 0.10,
    }

    def __init__(
        self,
        base_rate_limit: float = 2.0,
        distraction_probability: float = 0.10,
        distraction_range: tuple[float, float] = (2.0, 8.0),
    ):
        """
        Initialize the scheduler.

        Args:
            base_rate_limit: Minimum seconds between requests (default 2s)
            distraction_probability: Chance of adding extra delay (simulates human distraction)
            distraction_range: Range for random distraction delay in seconds
        """
        self.base_rate_limit = base_rate_limit
        self.distraction_probability = distraction_probability
        self.distraction_range = distraction_range
        self.last_request_time: float = 0.0

    @staticmethod
    def jitter(base_seconds: float, variance_pct: float = 0.3) -> float:
        """
        Add random variance to a time interval.

        Args:
            base_seconds: Base interval in seconds
            variance_pct: How much variance (0.3 = +/-30%)

        Returns:
            Jittered interval in seconds
        """
        min_val = base_seconds * (1 - variance_pct)
        max_val = base_seconds * (1 + variance_pct)
        return random.uniform(min_val, max_val)

    def rate_limit_wait(self) -> float:
        """
        Wait with randomized rate limiting between requests.

        Returns:
            Actual time waited in seconds
        """
        wait_time = self.jitter(self.base_rate_limit, variance_pct=0.5)

        # Occasionally add a longer pause (like a human getting distracted)
        if random.random() < self.distraction_probability:
            wait_time += random.uniform(*self.distraction_range)

        elapsed = time.time() - self.last_request_time
        actual_wait = max(0, wait_time - elapsed)

        if actual_wait > 0:
            time.sleep(actual_wait)

        self.last_request_time = time.time()
        return actual_wait

    def get_daily_sync_time(
        self, start_hour: int = 5, end_hour: int = 7
    ) -> datetime:
        """
        Get a randomized time for daily sync.

        Args:
            start_hour: Start of sync window (default 5am)
            end_hour: End of sync window (default 7am)

        Returns:
            datetime for next sync
        """
        tomorrow = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        random_hour = random.randint(start_hour, end_hour - 1)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        return tomorrow.replace(
            hour=random_hour, minute=random_minute, second=random_second
        )

    def get_weekly_sync_time(
        self, start_hour: int = 1, end_hour: int = 5
    ) -> datetime:
        """
        Get a randomized time for weekly sync on Sunday.

        Args:
            start_hour: Start of sync window (default 1am)
            end_hour: End of sync window (default 5am)

        Returns:
            datetime for next weekly sync
        """
        now = datetime.now()
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0 and now.hour >= end_hour:
            days_until_sunday = 7

        next_sunday = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=days_until_sunday)

        random_hour = random.randint(start_hour, end_hour - 1)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        return next_sunday.replace(
            hour=random_hour, minute=random_minute, second=random_second
        )

    def get_live_poll_interval(
        self, phase: TournamentPhase | str = TournamentPhase.ACTIVE
    ) -> float:
        """
        Get randomized interval for live tournament polling.

        Args:
            phase: Tournament phase (enum or string)

        Returns:
            Seconds until next poll
        """
        # Handle string input for backwards compatibility
        if isinstance(phase, str):
            try:
                phase = TournamentPhase(phase)
            except ValueError:
                phase = TournamentPhase.ACTIVE

        base = self.PHASE_INTERVALS.get(phase, 300)
        interval = self.jitter(base, variance_pct=0.4)

        # Occasionally skip a cycle (simulates connection issues)
        if random.random() < 0.05:
            interval *= random.uniform(1.5, 2.5)

        return interval

    def should_poll_now(self, phase: TournamentPhase | str = TournamentPhase.ACTIVE) -> bool:
        """
        Probabilistic decision on whether to poll.

        Args:
            phase: Tournament phase (enum or string)

        Returns:
            True if we should poll, False to skip this cycle
        """
        if isinstance(phase, str):
            try:
                phase = TournamentPhase(phase)
            except ValueError:
                phase = TournamentPhase.ACTIVE

        probability = self.POLL_PROBABILITY.get(phase, 1.0)
        return random.random() < probability


class OrganicRequestPattern:
    """
    Makes request patterns look more human-like by varying
    the order and timing of data fetches.
    """

    def __init__(self, scheduler: JitteredScheduler):
        """
        Initialize with a scheduler.

        Args:
            scheduler: JitteredScheduler instance for timing
        """
        self.scheduler = scheduler

    def batch_with_breaks(
        self,
        items: list[T],
        process_func: Callable[[T], Any],
        batch_size: int = 5,
        break_base: float = 10.0,
        long_break_probability: float = 0.15,
        long_break_range: tuple[float, float] = (20.0, 60.0),
    ) -> list[Any]:
        """
        Process items in batches with random breaks between batches.

        Args:
            items: List of items to process
            process_func: Function to call for each item
            batch_size: Approximate batch size (will vary +/-40%)
            break_base: Base break time between batches (seconds)
            long_break_probability: Chance of taking a longer break
            long_break_range: Range for long break duration

        Returns:
            List of results from process_func
        """
        results: list[Any] = []
        items_list = list(items)

        # Shuffle order to avoid predictable patterns
        random.shuffle(items_list)

        i = 0
        while i < len(items_list):
            # Vary batch size
            current_batch_size = max(1, int(self.scheduler.jitter(batch_size, 0.4)))
            batch = items_list[i : i + current_batch_size]

            for item in batch:
                self.scheduler.rate_limit_wait()
                result = process_func(item)
                results.append(result)

            i += current_batch_size

            # Take a break between batches
            if i < len(items_list):
                break_time = self.scheduler.jitter(break_base, 0.5)
                if random.random() < long_break_probability:
                    break_time += random.uniform(*long_break_range)
                time.sleep(break_time)

        return results

    @staticmethod
    def shuffle_tasks(sync_tasks: list[T]) -> list[T]:
        """
        Randomize the order of sync tasks.

        Args:
            sync_tasks: List of tasks (e.g., (name, function) tuples)

        Returns:
            Shuffled copy of the list
        """
        tasks = list(sync_tasks)
        random.shuffle(tasks)
        return tasks

    # Backwards compatibility alias
    def get_sync_order(self, sync_tasks: list[T]) -> list[T]:
        """Alias for shuffle_tasks (deprecated)."""
        return self.shuffle_tasks(sync_tasks)


class TournamentPhaseDetector:
    """Determines what phase a tournament is in to adjust polling frequency."""

    # Tournament status constants
    STATUS_UPCOMING = "UPCOMING"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"

    # Round status constants
    ROUND_SUSPENDED = "SUSPENDED"
    ROUND_COMPLETE = "COMPLETE"

    @classmethod
    def get_phase(
        cls,
        tournament_status: str,
        current_hour: int | None = None,
        round_status: str | None = None,
    ) -> TournamentPhase:
        """
        Determine tournament phase for polling decisions.

        Args:
            tournament_status: UPCOMING, IN_PROGRESS, COMPLETED
            current_hour: Current hour (0-23), defaults to now
            round_status: IN_PROGRESS, SUSPENDED, COMPLETE, etc.

        Returns:
            TournamentPhase enum value
        """
        if tournament_status != cls.STATUS_IN_PROGRESS:
            return TournamentPhase.INACTIVE

        if current_hour is None:
            current_hour = datetime.now().hour

        # Night hours (roughly when no play happens)
        # Tournaments typically run 7am-7pm local time
        if current_hour < 6 or current_hour > 20:
            return TournamentPhase.NIGHT

        if round_status == cls.ROUND_SUSPENDED:
            return TournamentPhase.WEATHER_DELAY

        if round_status == cls.ROUND_COMPLETE:
            return TournamentPhase.BETWEEN_ROUNDS

        return TournamentPhase.ACTIVE


# Convenience functions


def sleep_with_jitter(base_seconds: float, variance_pct: float = 0.3) -> float:
    """
    Sleep for a jittered duration.

    Args:
        base_seconds: Base sleep duration
        variance_pct: Variance percentage (+/- this percentage)

    Returns:
        Actual sleep duration
    """
    jittered = JitteredScheduler.jitter(base_seconds, variance_pct)
    time.sleep(jittered)
    return jittered


def random_time_in_window(start_hour: int, end_hour: int) -> tuple[int, int]:
    """
    Get random hour:minute within a time window.

    Args:
        start_hour: Start of window (inclusive)
        end_hour: End of window (exclusive)

    Returns:
        Tuple of (hour, minute)
    """
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    return (hour, minute)


# Default configuration
DEFAULT_CONFIG = {
    "min_request_interval": 2.0,
    "daily_sync_window": {"start_hour": 5, "end_hour": 7},
    "weekly_sync_window": {"start_hour": 1, "end_hour": 5},
    "live_polling": {
        "active_play": 180,
        "between_rounds": 600,
        "weather_delay": 900,
        "night": 1800,
    },
    "jitter": {"request_variance": 0.5, "interval_variance": 0.4},
    "skip_probability": {
        "active": 0.05,
        "between_rounds": 0.20,
        "weather_delay": 0.40,
        "night": 0.70,
    },
}


if __name__ == "__main__":
    scheduler = JitteredScheduler()

    print("=== Jittered Scheduler Demo ===\n")

    print("Daily sync times (next 7 days):")
    for i in range(7):
        sync_time = scheduler.get_daily_sync_time()
        print(f"  Day {i + 1}: {sync_time.strftime('%A %I:%M:%S %p')}")
        time.sleep(0.01)

    print("\nLive poll intervals (active play):")
    for i in range(10):
        interval = scheduler.get_live_poll_interval(TournamentPhase.ACTIVE)
        print(f"  Poll {i + 1}: {interval:.1f}s ({interval / 60:.1f} min)")

    print("\nLive poll intervals (night):")
    for i in range(5):
        interval = scheduler.get_live_poll_interval(TournamentPhase.NIGHT)
        print(f"  Poll {i + 1}: {interval:.1f}s ({interval / 60:.1f} min)")

    print("\nPhase detection examples:")
    detector = TournamentPhaseDetector()
    test_cases = [
        ("IN_PROGRESS", 14, None),
        ("IN_PROGRESS", 3, None),
        ("IN_PROGRESS", 14, "SUSPENDED"),
        ("COMPLETED", 14, None),
    ]
    for status, hour, round_status in test_cases:
        phase = detector.get_phase(status, hour, round_status)
        print(f"  status={status}, hour={hour}, round={round_status} -> {phase.value}")
