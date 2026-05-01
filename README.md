# Binance Futures Testnet Trading Bot

Python CLI application to place and manage Binance Futures Testnet orders with validation, logging, and robust error handling.

## Features

- Place `MARKET` orders
- Place `LIMIT` orders
- Supports `BUY` and `SELL`
- CLI-based input using `argparse`
- Input validation for side, type, quantity, and price rules
- Logging of API requests and responses
- Error handling for validation, API, and network failures

## Tech Stack

- Python 3
- `python-binance`
- `python-dotenv`
- `argparse`
- `logging`

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
  requirements.txt
  README.md
```

## Setup Instructions

1. Clone the repository:

```bash
git clone <your-repo-url>
cd trading_bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```

## Usage Examples

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 80000
```

## Sample Output

```text
=== Order Request Summary ===
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01
Price: N/A

=== Order Response ===
Order ID: 13096138224
Status: FILLED
Executed Qty: 0.0100
Average Price: 68123.45
```

## Logging

- Logs are saved in `trading_bot.log`
- Log entries include:
  - API request parameters
  - API responses
  - Errors with stack traces

## Assumptions

- Uses Binance Futures Testnet
- No real money involved
- API keys are required in `.env`

## Notes

- LIMIT orders may remain `NEW` until the requested price is reached
- MARKET orders execute immediately under normal market conditions
