"""
Configuration management for PGA Tour data sync service.

Centralizes all configuration values with environment variable support and validation.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    pool_min_connections: int = 1
    pool_max_connections: int = 10
    connection_timeout: int = 30
    batch_size: int = 100

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Load database configuration from environment variables."""
        url = os.getenv('DATABASE_URL')
        if not url:
            raise ValueError("DATABASE_URL environment variable not set")

        return cls(
            url=url,
            pool_min_connections=int(os.getenv('DB_POOL_MIN', '1')),
            pool_max_connections=int(os.getenv('DB_POOL_MAX', '10')),
            connection_timeout=int(os.getenv('DB_TIMEOUT', '30')),
            batch_size=int(os.getenv('DB_BATCH_SIZE', '100'))
        )


@dataclass
class APIConfig:
    """PGA Tour API configuration settings."""
    key: str
    url: str = "https://orchestrator.pgatour.com/graphql"
    timeout: int = 30
    max_retries: int = 3
    base_rate_limit: float = 2.0

    @classmethod
    def from_env(cls) -> 'APIConfig':
        """Load API configuration from environment variables."""
        key = os.getenv('PGA_TOUR_API_KEY')
        if not key:
            raise ValueError("PGA_TOUR_API_KEY environment variable not set")

        return cls(
            key=key,
            url=os.getenv('PGA_API_URL', 'https://orchestrator.pgatour.com/graphql'),
            timeout=int(os.getenv('PGA_API_TIMEOUT', '30')),
            max_retries=int(os.getenv('PGA_API_RETRIES', '3')),
            base_rate_limit=float(os.getenv('PGA_API_RATE_LIMIT', '2.0'))
        )


@dataclass
class SyncConfig:
    """Sync job configuration settings."""
    # Snapshot retention
    snapshot_retention_days: int = 30

    # Tournament field sync
    field_sync_days_ahead: int = 14

    # Results sync
    results_batch_size: int = 20

    # Polling configuration
    poll_active_interval: int = 180  # 3 minutes
    poll_between_rounds_interval: int = 600  # 10 minutes
    poll_weather_delay_interval: int = 900  # 15 minutes
    poll_night_interval: int = 1800  # 30 minutes
    poll_inactive_interval: int = 3600  # 1 hour

    # Polling probabilities (0.0 to 1.0)
    poll_active_probability: float = 0.95
    poll_between_rounds_probability: float = 0.80
    poll_weather_delay_probability: float = 0.60
    poll_night_probability: float = 0.30
    poll_inactive_probability: float = 0.10

    @classmethod
    def from_env(cls) -> 'SyncConfig':
        """Load sync configuration from environment variables."""
        return cls(
            snapshot_retention_days=int(os.getenv('SYNC_SNAPSHOT_RETENTION_DAYS', '30')),
            field_sync_days_ahead=int(os.getenv('SYNC_FIELD_DAYS_AHEAD', '14')),
            results_batch_size=int(os.getenv('SYNC_RESULTS_BATCH', '20')),
            poll_active_interval=int(os.getenv('POLL_ACTIVE_INTERVAL', '180')),
            poll_between_rounds_interval=int(os.getenv('POLL_BETWEEN_ROUNDS_INTERVAL', '600')),
            poll_weather_delay_interval=int(os.getenv('POLL_WEATHER_DELAY_INTERVAL', '900')),
            poll_night_interval=int(os.getenv('POLL_NIGHT_INTERVAL', '1800')),
            poll_inactive_interval=int(os.getenv('POLL_INACTIVE_INTERVAL', '3600')),
            poll_active_probability=float(os.getenv('POLL_ACTIVE_PROB', '0.95')),
            poll_between_rounds_probability=float(os.getenv('POLL_BETWEEN_ROUNDS_PROB', '0.80')),
            poll_weather_delay_probability=float(os.getenv('POLL_WEATHER_DELAY_PROB', '0.60')),
            poll_night_probability=float(os.getenv('POLL_NIGHT_PROB', '0.30')),
            poll_inactive_probability=float(os.getenv('POLL_INACTIVE_PROB', '0.10'))
        )


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_dir: str = "logs"
    max_log_file_size_mb: int = 10
    max_log_backups: int = 5

    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """Load logging configuration from environment variables."""
        return cls(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            log_dir=os.getenv('LOG_DIR', 'logs'),
            max_log_file_size_mb=int(os.getenv('LOG_MAX_SIZE_MB', '10')),
            max_log_backups=int(os.getenv('LOG_MAX_BACKUPS', '5'))
        )


@dataclass
class Config:
    """Main configuration container."""
    database: DatabaseConfig
    api: APIConfig
    sync: SyncConfig
    logging: LoggingConfig
    environment: str = "production"

    @classmethod
    def from_env(cls) -> 'Config':
        """Load all configuration from environment variables."""
        return cls(
            database=DatabaseConfig.from_env(),
            api=APIConfig.from_env(),
            sync=SyncConfig.from_env(),
            logging=LoggingConfig.from_env(),
            environment=os.getenv('ENVIRONMENT', 'production')
        )

    def validate(self) -> None:
        """Validate configuration values."""
        # Database validation
        if self.database.pool_min_connections < 1:
            raise ValueError("DB_POOL_MIN must be >= 1")
        if self.database.pool_max_connections < self.database.pool_min_connections:
            raise ValueError("DB_POOL_MAX must be >= DB_POOL_MIN")
        if self.database.connection_timeout < 1:
            raise ValueError("DB_TIMEOUT must be >= 1")

        # API validation
        if self.api.timeout < 1:
            raise ValueError("PGA_API_TIMEOUT must be >= 1")
        if self.api.max_retries < 0:
            raise ValueError("PGA_API_RETRIES must be >= 0")
        if self.api.base_rate_limit < 0:
            raise ValueError("PGA_API_RATE_LIMIT must be >= 0")

        # Sync validation
        if self.sync.snapshot_retention_days < 1:
            raise ValueError("SYNC_SNAPSHOT_RETENTION_DAYS must be >= 1")
        if not (0 <= self.sync.poll_active_probability <= 1):
            raise ValueError("Poll probabilities must be between 0 and 1")


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config instance

    Raises:
        ValueError: If configuration is invalid
    """
    global _config
    if _config is None:
        _config = Config.from_env()
        _config.validate()
    return _config


def reset_config() -> None:
    """Reset the global configuration instance (useful for testing)."""
    global _config
    _config = None
