"""CLI entrypoint for Binance Futures Testnet order placement."""

from __future__ import annotations

import argparse
import sys

from binance.exceptions import BinanceAPIException, BinanceRequestException
from requests.exceptions import RequestException

from bot.client import BinanceFuturesClient, ConfigurationError
from bot.logging_config import setup_logging
from bot.orders import OrderService
from bot.validators import ValidationError, ValidatedOrderInput, validate_order_inputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet MARKET or LIMIT orders."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity (> 0)")
    parser.add_argument("--price", type=float, help="Order price (required for LIMIT only)")
    return parser


def _display_value(value: object) -> str:
    if value in (None, ""):
        return "N/A"
    return str(value)


def print_order_summary(order_input: ValidatedOrderInput, response: dict) -> None:
    print("=" * 44)
    print("Order Request Summary")
    print("=" * 44)
    print(f"{'Symbol':<18}: {_display_value(order_input.symbol)}")
    print(f"{'Side':<18}: {_display_value(order_input.side)}")
    print(f"{'Type':<18}: {_display_value(order_input.order_type)}")
    print(f"{'Quantity':<18}: {_display_value(order_input.quantity)}")
    print(f"{'Price':<18}: {_display_value(order_input.price)}")

    print()
    print("=" * 44)
    print("Order Response")
    print("=" * 44)
    print(f"{'Order ID':<18}: {_display_value(response.get('orderId'))}")
    print(f"{'Status':<18}: {_display_value(response.get('status'))}")
    print(f"{'Executed Qty':<18}: {_display_value(response.get('executedQty'))}")
    print(f"{'Average Price':<18}: {_display_value(response.get('avgPrice'))}")


def main() -> int:
    logger = setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    try:
        validated = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        client = BinanceFuturesClient()
        service = OrderService(client)
        response = service.place_order(validated)
        print_order_summary(validated, response)
        return 0

    except ValidationError as exc:
        logger.error("Validation error: %s", str(exc), exc_info=True)
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    except ConfigurationError as exc:
        logger.error("Configuration error: %s", str(exc), exc_info=True)
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except BinanceAPIException as exc:
        logger.error("Binance API error: %s", str(exc), exc_info=True)
        print("Binance API error: Unable to place order. Check symbol, balance, and parameters.", file=sys.stderr)
        return 1
    except (BinanceRequestException, RequestException) as exc:
        logger.error("Network/request error: %s", str(exc), exc_info=True)
        print("Network error: Could not reach Binance API. Please try again.", file=sys.stderr)
        return 1
    except Exception as exc:
        logger.exception("Unexpected error while placing order: %s", str(exc))
        print("Unexpected error: Failed to place order. See trading_bot.log for details.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
