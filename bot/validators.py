"""Validation utilities for CLI trading inputs."""

from __future__ import annotations

from dataclasses import dataclass


ALLOWED_SIDES = {"BUY", "SELL"}
ALLOWED_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    """Raised when user input validation fails."""


@dataclass(frozen=True)
class ValidatedOrderInput:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None


def _normalize_upper(value: str, field_name: str) -> str:
    normalized = (value or "").strip().upper()
    if not normalized:
        raise ValidationError(f"{field_name} cannot be empty.")
    return normalized


def _validate_positive_number(value: float | None, field_name: str) -> float:
    if value is None:
        raise ValidationError(f"{field_name} is required.")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc
    if number <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return number


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> ValidatedOrderInput:
    """
    Validate and normalize order inputs from CLI arguments.
    """
    normalized_symbol = _normalize_upper(symbol, "Symbol")
    normalized_side = _normalize_upper(side, "Side")
    normalized_type = _normalize_upper(order_type, "Type")

    if normalized_side not in ALLOWED_SIDES:
        raise ValidationError("Invalid side. Allowed values: BUY, SELL.")

    if normalized_type not in ALLOWED_ORDER_TYPES:
        raise ValidationError("Invalid type. Allowed values: MARKET, LIMIT.")

    validated_quantity = _validate_positive_number(quantity, "Quantity")

    validated_price: float | None = None
    if normalized_type == "LIMIT":
        validated_price = _validate_positive_number(price, "Price")
    elif price is not None:
        # Explicitly reject price for market orders to avoid accidental misuse.
        raise ValidationError("Price must not be provided for MARKET orders.")

    return ValidatedOrderInput(
        symbol=normalized_symbol,
        side=normalized_side,
        order_type=normalized_type,
        quantity=validated_quantity,
        price=validated_price,
    )
