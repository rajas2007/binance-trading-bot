"""Binance Futures Testnet client wrapper."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from binance.client import Client
from dotenv import load_dotenv

from bot.logging_config import setup_logging


FUTURES_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
FUTURES_TESTNET_API_URL = f"{FUTURES_TESTNET_BASE_URL}/fapi"


class ConfigurationError(RuntimeError):
    """Raised when required runtime configuration is missing."""


class BinanceFuturesClient:
    """
    Encapsulates Binance API client initialization and API call logging.
    """

    def __init__(self) -> None:
        self.logger = setup_logging()
        self.client = self._create_client()

    @staticmethod
    def _normalize_env_value(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip().strip('"').strip("'")
        return cleaned or None

    def _create_client(self) -> Client:
        project_root = Path(__file__).resolve().parent.parent
        env_path = project_root / ".env"
        # Override shell vars so project-local .env is authoritative.
        load_dotenv(dotenv_path=env_path, override=True)

        api_key = self._normalize_env_value(os.getenv("BINANCE_API_KEY"))
        api_secret = self._normalize_env_value(os.getenv("BINANCE_API_SECRET"))

        if not api_key or not api_secret:
            raise ConfigurationError(
                "Missing Binance credentials. Set BINANCE_API_KEY and "
                "BINANCE_API_SECRET environment variables with non-empty values."
            )

        client = Client(api_key=api_key, api_secret=api_secret)
        # Force Futures requests to go only to Binance Futures Testnet.
        client.FUTURES_URL = FUTURES_TESTNET_API_URL

        self.logger.info("Initialized Binance Futures client for testnet: %s", FUTURES_TESTNET_BASE_URL)
        return client

    def create_futures_order(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Call futures_create_order while logging request, response, and errors.
        """
        self.logger.info("API Request | futures_create_order | params=%s", params)
        try:
            response = self.client.futures_create_order(**params)
            self.logger.info("API Response | futures_create_order | response=%s", response)
            return response
        except Exception as exc:
            self.logger.error(
                "API Error | futures_create_order failed | error=%s",
                str(exc),
                exc_info=True,
            )
            raise

    def get_futures_order(self, symbol: str, order_id: int | str) -> dict[str, Any]:
        """
        Fetch the latest state of a futures order using symbol and orderId.
        """
        request_params = {"symbol": symbol, "orderId": order_id}
        self.logger.info("API Request | futures_get_order | params=%s", request_params)
        try:
            response = self.client.futures_get_order(**request_params)
            self.logger.info("API Response | futures_get_order | response=%s", response)
            return response
        except Exception as exc:
            self.logger.error(
                "API Error | futures_get_order failed | error=%s",
                str(exc),
                exc_info=True,
            )
            raise
