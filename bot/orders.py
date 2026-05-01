"""Order business logic for futures trading."""

from __future__ import annotations

import time
from typing import Any

from binance.exceptions import BinanceAPIException

from bot.client import BinanceFuturesClient
from bot.validators import ValidatedOrderInput


class OrderService:
    """Builds and submits orders through the Binance futures client."""

    def __init__(self, api_client: BinanceFuturesClient) -> None:
        self.api_client = api_client

    def _fetch_latest_order_state(
        self,
        symbol: str,
        order_id: int | str,
        attempts: int = 5,
        delay_seconds: float = 0.3,
    ) -> dict[str, Any] | None:
        """
        Poll futures_get_order briefly because immediate reads can return -2013.
        """
        for attempt in range(attempts):
            try:
                return self.api_client.get_futures_order(symbol=symbol, order_id=order_id)
            except BinanceAPIException as exc:
                error_text = str(exc)
                is_order_not_ready = "code=-2013" in error_text or "Order does not exist" in error_text
                if not is_order_not_ready or attempt == attempts - 1:
                    raise
                time.sleep(delay_seconds)
        return None

    def place_order(self, order_input: ValidatedOrderInput) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": order_input.symbol,
            "side": order_input.side,
            "type": order_input.order_type,
            "quantity": order_input.quantity,
        }

        if order_input.order_type == "LIMIT":
            params["price"] = order_input.price
            params["timeInForce"] = "GTC"

        create_response = self.api_client.create_futures_order(params=params)
        order_id = create_response.get("orderId")
        if order_id in (None, ""):
            return create_response
        latest_response = self._fetch_latest_order_state(
            symbol=order_input.symbol,
            order_id=order_id,
        )
        return latest_response or create_response
