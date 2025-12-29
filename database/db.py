"""
Database connection utilities for PGA Tour data sync service.

Provides context managers for database connections and connection pooling.
"""

import os
import psycopg2
from psycopg2 import pool, extras, OperationalError
from contextlib import contextmanager
from typing import Optional, Dict, Any, List, Tuple, Union
from dotenv import load_dotenv
import logging
import time

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database errors."""
    pass


class DatabasePool:
    """Connection pool manager for PostgreSQL database."""

    _pool: Optional[pool.SimpleConnectionPool] = None
    _initialized: bool = False

    @classmethod
    def initialize(cls, minconn: int = 1, maxconn: int = 10, timeout: int = 30) -> None:
        """
        Initialize the connection pool.

        Args:
            minconn: Minimum number of connections in pool
            maxconn: Maximum number of connections in pool
            timeout: Connection timeout in seconds

        Raises:
            DatabaseError: If pool initialization fails
        """
        if cls._pool is not None:
            logger.warning("Database pool already initialized")
            return

        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise DatabaseError("DATABASE_URL environment variable not set")

        try:
            cls._pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                database_url,
                connect_timeout=timeout
            )
            cls._initialized = True
            logger.info(f"Database pool initialized (min={minconn}, max={maxconn}, timeout={timeout}s)")
        except Exception as e:
            raise DatabaseError(f"Failed to initialize database pool: {e}") from e

    @classmethod
    def get_connection(cls, retry_count: int = 3, retry_delay: float = 1.0):
        """
        Get a connection from the pool with retry logic.

        Args:
            retry_count: Number of times to retry on failure
            retry_delay: Delay between retries in seconds

        Returns:
            Database connection

        Raises:
            DatabaseError: If unable to get connection after retries
        """
        if cls._pool is None:
            cls.initialize()

        last_error = None
        for attempt in range(retry_count):
            try:
                conn = cls._pool.getconn()
                # Test connection is alive
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return conn
            except OperationalError as e:
                last_error = e
                logger.warning(f"Connection attempt {attempt + 1}/{retry_count} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
            except Exception as e:
                raise DatabaseError(f"Unexpected error getting connection: {e}") from e

        raise DatabaseError(f"Failed to get connection after {retry_count} attempts") from last_error

    @classmethod
    def return_connection(cls, conn, close_on_error: bool = True) -> None:
        """
        Return a connection to the pool.

        Args:
            conn: Connection to return
            close_on_error: Whether to close connection if it's in error state
        """
        if cls._pool is None:
            logger.warning("Cannot return connection - pool not initialized")
            return

        try:
            # Check if connection is in a bad state
            if conn.closed or (close_on_error and conn.info.transaction_status == psycopg2.extensions.TRANSACTION_STATUS_INERROR):
                conn.close()
                logger.warning("Closed bad connection instead of returning to pool")
            else:
                cls._pool.putconn(conn)
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")

    @classmethod
    def close_all(cls) -> None:
        """Close all connections in the pool."""
        if cls._pool is not None:
            try:
                cls._pool.closeall()
                cls._pool = None
                cls._initialized = False
                logger.info("Database pool closed")
            except Exception as e:
                logger.error(f"Error closing database pool: {e}")

    @classmethod
    def health_check(cls) -> bool:
        """
        Check if database connection is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.

    Usage:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM players")
                rows = cur.fetchall()
    """
    conn = DatabasePool.get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        DatabasePool.return_connection(conn)


@contextmanager
def get_db_cursor(cursor_factory=None):
    """
    Context manager for database cursor.

    Usage:
        with get_db_cursor() as cur:
            cur.execute("SELECT * FROM players")
            rows = cur.fetchall()
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
        finally:
            cursor.close()


def execute_query(query: str, params: Optional[Union[Tuple, List]] = None, fetch: bool = True) -> Optional[List]:
    """
    Execute a query and return results.

    Args:
        query: SQL query string
        params: Query parameters (tuple or list)
        fetch: Whether to fetch results (True) or just execute (False)

    Returns:
        List of rows if fetch=True, None otherwise

    Raises:
        DatabaseError: If query execution fails
    """
    try:
        with get_db_cursor() as cur:
            cur.execute(query, params or ())
            if fetch:
                return cur.fetchall()
        return None
    except Exception as e:
        logger.error(f"Query execution failed: {e}\nQuery: {query}\nParams: {params}")
        raise DatabaseError(f"Query execution failed: {e}") from e


def execute_dict_query(query: str, params: Optional[Union[Tuple, List]] = None) -> List[Dict[str, Any]]:
    """
    Execute a query and return results as list of dictionaries.

    Args:
        query: SQL query string
        params: Query parameters (tuple or list)

    Returns:
        List of dictionaries with column names as keys

    Raises:
        DatabaseError: If query execution fails
    """
    try:
        with get_db_cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    except Exception as e:
        logger.error(f"Dict query execution failed: {e}\nQuery: {query}\nParams: {params}")
        raise DatabaseError(f"Dict query execution failed: {e}") from e


def upsert_records(table: str, records: List[Dict[str, Any]], conflict_columns: List[str],
                   update_columns: Optional[List[str]] = None, batch_size: int = 100) -> int:
    """
    Insert or update multiple records using PostgreSQL's ON CONFLICT.

    Args:
        table: Table name (must be a valid identifier)
        records: List of dictionaries representing records
        conflict_columns: Columns that determine uniqueness (for ON CONFLICT)
        update_columns: Columns to update on conflict (None = update all except conflict columns)
        batch_size: Number of records to process per batch

    Returns:
        Number of records affected

    Raises:
        DatabaseError: If upsert operation fails
        ValueError: If input validation fails
    """
    if not records:
        return 0

    # Validate table name (simple check to prevent SQL injection)
    if not table.replace('_', '').isalnum():
        raise ValueError(f"Invalid table name: {table}")

    # Validate all records have same schema
    columns = list(records[0].keys())
    for i, record in enumerate(records[1:], 1):
        if set(record.keys()) != set(columns):
            raise ValueError(f"Record {i} has different columns than first record")

    # Validate conflict columns exist
    for col in conflict_columns:
        if col not in columns:
            raise ValueError(f"Conflict column '{col}' not found in record columns")

    # Determine which columns to update on conflict
    if update_columns is None:
        update_columns = [col for col in columns if col not in conflict_columns]
    else:
        # Validate update columns
        for col in update_columns:
            if col not in columns:
                raise ValueError(f"Update column '{col}' not found in record columns")

    if not update_columns:
        logger.warning(f"No columns to update on conflict for table {table}")

    # Build the INSERT statement
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    conflict_str = ', '.join(conflict_columns)
    update_str = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_columns])

    if update_columns:
        # Also update updated_at if it exists
        if 'updated_at' in columns and 'updated_at' not in update_columns:
            update_str += ", updated_at = NOW()"

        query = f"""
            INSERT INTO {table} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_str})
            DO UPDATE SET {update_str}
        """
    else:
        query = f"""
            INSERT INTO {table} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_str})
            DO NOTHING
        """

    # Prepare values
    values = [[record.get(col) for col in columns] for record in records]

    try:
        total_affected = 0
        with get_db_cursor() as cur:
            # Process in batches
            for i in range(0, len(values), batch_size):
                batch = values[i:i + batch_size]
                extras.execute_batch(cur, query, batch, page_size=batch_size)
                total_affected += len(batch)

        logger.debug(f"Upserted {total_affected} records into {table}")
        return total_affected

    except Exception as e:
        logger.error(f"Upsert failed for table {table}: {e}")
        raise DatabaseError(f"Upsert failed for table {table}: {e}") from e


def log_sync(operation: str, status: str, records_affected: int = 0,
             error_message: Optional[str] = None) -> int:
    """
    Log a sync operation to the sync_log table.

    Args:
        operation: Name of the sync operation (e.g., 'players_sync', 'schedule_sync')
        status: Status of the operation ('success', 'error', 'in_progress')
        records_affected: Number of records affected
        error_message: Error message if status is 'error'

    Returns:
        ID of the created log entry
    """
    query = """
        INSERT INTO sync_log (operation, status, records_affected, error_message)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """
    with get_db_cursor() as cur:
        cur.execute(query, (operation, status, records_affected, error_message))
        return cur.fetchone()[0]


def get_last_sync(operation: str) -> Optional[Dict[str, Any]]:
    """
    Get the last sync log entry for a given operation.

    Args:
        operation: Name of the sync operation

    Returns:
        Dictionary with sync log data or None if no previous sync
    """
    query = """
        SELECT id, operation, status, records_affected, error_message, synced_at
        FROM sync_log
        WHERE operation = %s
        ORDER BY synced_at DESC
        LIMIT 1
    """
    results = execute_dict_query(query, (operation,))
    return results[0] if results else None
