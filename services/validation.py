"""
Data validation utilities for PGA Tour data.

Provides validation functions to ensure data quality before database insertion.
"""

import re
from decimal import Decimal, InvalidOperation
from datetime import datetime, date
from typing import Any, Optional, List, Dict


class ValidationError(Exception):
    """Exception raised for data validation errors."""
    pass


def validate_player_id(player_id: Any) -> str:
    """
    Validate player ID format.

    Args:
        player_id: Player ID to validate

    Returns:
        Validated player ID as string

    Raises:
        ValidationError: If player ID is invalid
    """
    if not player_id:
        raise ValidationError("Player ID cannot be empty")

    player_id = str(player_id).strip()

    if not player_id.isdigit():
        raise ValidationError(f"Invalid player ID format: {player_id}")

    return player_id


def validate_tournament_id(tournament_id: Any) -> str:
    """
    Validate tournament ID format.

    Expected format: {Tour}{Year}{Number} (e.g., R2024016)

    Args:
        tournament_id: Tournament ID to validate

    Returns:
        Validated tournament ID as string

    Raises:
        ValidationError: If tournament ID is invalid
    """
    if not tournament_id:
        raise ValidationError("Tournament ID cannot be empty")

    tournament_id = str(tournament_id).strip()

    # Format: R2024016 (Letter + 4-digit year + 3-digit number)
    if not re.match(r'^[A-Z]\d{7}$', tournament_id):
        raise ValidationError(f"Invalid tournament ID format: {tournament_id} (expected format: R2024016)")

    return tournament_id


def validate_money(money: Any, allow_negative: bool = False) -> Decimal:
    """
    Validate and parse money value.

    Args:
        money: Money value (string, int, float, or Decimal)
        allow_negative: Whether negative values are allowed

    Returns:
        Validated money as Decimal

    Raises:
        ValidationError: If money value is invalid
    """
    if money is None:
        return Decimal("0")

    try:
        # Handle string with currency symbols
        if isinstance(money, str):
            cleaned = money.replace("$", "").replace(",", "").strip()
            if not cleaned:
                return Decimal("0")
            value = Decimal(cleaned)
        else:
            value = Decimal(str(money))

        # Validate range
        if not allow_negative and value < 0:
            raise ValidationError(f"Money value cannot be negative: {money}")

        # Reasonable upper bound (max tournament purse ~$25M)
        if value > Decimal("100000000"):  # $100M
            raise ValidationError(f"Money value unreasonably large: {money}")

        return value

    except (ValueError, InvalidOperation) as e:
        raise ValidationError(f"Invalid money value: {money}") from e


def validate_position(position: Any) -> tuple[str, Optional[int]]:
    """
    Validate and parse position string.

    Args:
        position: Position value (e.g., "1", "T5", "CUT")

    Returns:
        Tuple of (position_string, numeric_position or None)

    Raises:
        ValidationError: If position is invalid
    """
    if not position:
        return ("", None)

    position_str = str(position).strip().upper()

    # Valid non-finish positions
    NON_FINISH = {"CUT", "MC", "WD", "DQ", "W/D", "DNS", "MDF"}
    if position_str in NON_FINISH:
        return (position_str, None)

    # Try to extract numeric value
    try:
        # Remove 'T' prefix if present (tied position)
        numeric_str = position_str.lstrip("T").strip()
        numeric_val = int(numeric_str)

        if numeric_val < 1 or numeric_val > 200:
            raise ValidationError(f"Position number out of valid range (1-200): {position}")

        return (position_str, numeric_val)

    except ValueError:
        # Invalid format
        raise ValidationError(f"Invalid position format: {position}")


def validate_date(date_val: Any) -> Optional[date]:
    """
    Validate and parse date value.

    Args:
        date_val: Date value (string, datetime, or date)

    Returns:
        Validated date or None

    Raises:
        ValidationError: If date is invalid
    """
    if date_val is None:
        return None

    if isinstance(date_val, date):
        return date_val

    if isinstance(date_val, datetime):
        return date_val.date()

    if isinstance(date_val, str):
        # Try common date formats
        date_str = date_val.strip()
        if not date_str:
            return None

        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y/%m/%d"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue

        raise ValidationError(f"Invalid date format: {date_val}")

    raise ValidationError(f"Invalid date type: {type(date_val)}")


def validate_tour_code(tour_code: Any) -> str:
    """
    Validate tour code.

    Args:
        tour_code: Tour code to validate

    Returns:
        Validated tour code

    Raises:
        ValidationError: If tour code is invalid
    """
    if not tour_code:
        raise ValidationError("Tour code cannot be empty")

    tour_code = str(tour_code).strip().upper()

    VALID_TOURS = {"R", "H", "M", "S", "C", "E"}
    if tour_code not in VALID_TOURS:
        raise ValidationError(f"Invalid tour code: {tour_code} (valid: {', '.join(sorted(VALID_TOURS))})")

    return tour_code


def validate_year(year: Any, min_year: int = 2000, max_year: int = 2100) -> int:
    """
    Validate year value.

    Args:
        year: Year to validate
        min_year: Minimum valid year
        max_year: Maximum valid year

    Returns:
        Validated year as integer

    Raises:
        ValidationError: If year is invalid
    """
    if year is None:
        raise ValidationError("Year cannot be None")

    try:
        year_int = int(year)
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid year value: {year}") from e

    if not (min_year <= year_int <= max_year):
        raise ValidationError(f"Year out of valid range ({min_year}-{max_year}): {year}")

    return year_int


def validate_player_data(player: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate player data dictionary.

    Args:
        player: Player data dictionary

    Returns:
        Validated player data

    Raises:
        ValidationError: If player data is invalid
    """
    if not isinstance(player, dict):
        raise ValidationError("Player data must be a dictionary")

    if "id" not in player:
        raise ValidationError("Player data missing required field: id")

    validated = {
        "id": validate_player_id(player["id"]),
        "first_name": str(player.get("first_name", "")).strip() or str(player.get("firstName", "")).strip(),
        "last_name": str(player.get("last_name", "")).strip() or str(player.get("lastName", "")).strip(),
        "display_name": str(player.get("display_name", "")).strip() or str(player.get("displayName", "")).strip(),
        "country": player.get("country"),
        "country_flag": player.get("country_flag") or player.get("countryFlag"),
        "headshot_url": player.get("headshot_url") or player.get("headshot"),
        "is_active": bool(player.get("is_active", True) if "is_active" in player else player.get("isActive", True))
    }

    # Ensure we have at least a display name
    if not validated["display_name"]:
        if validated["first_name"] or validated["last_name"]:
            validated["display_name"] = f"{validated['first_name']} {validated['last_name']}".strip()
        else:
            raise ValidationError(f"Player {validated['id']} has no name information")

    return validated


def validate_non_empty_string(value: Any, field_name: str, max_length: Optional[int] = None) -> str:
    """
    Validate that a value is a non-empty string.

    Args:
        value: Value to validate
        field_name: Name of the field (for error messages)
        max_length: Optional maximum length

    Returns:
        Validated string

    Raises:
        ValidationError: If validation fails
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{field_name} cannot be empty")

    value_str = str(value).strip()

    if max_length and len(value_str) > max_length:
        raise ValidationError(f"{field_name} exceeds maximum length of {max_length}")

    return value_str


def sanitize_for_db(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize data dictionary for database insertion.

    Removes None values from nested objects, trims strings, etc.

    Args:
        data: Data dictionary to sanitize

    Returns:
        Sanitized data dictionary
    """
    sanitized = {}

    for key, value in data.items():
        if value is None:
            sanitized[key] = None
        elif isinstance(value, str):
            sanitized[key] = value.strip() if value.strip() else None
        elif isinstance(value, dict):
            sanitized[key] = sanitize_for_db(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_for_db(item) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value

    return sanitized
