# algofin
## Back test trading algorithms

Create an algorithm and back test it against historical pricing data

### Algorithm properties
An algorithm has specific features that can be configured.
- strategy_name
- description
- buy_offset: at what percentage (<=1) of the current price to enter a limit buy order
- sell_offset: after a successful purchase, at what percentage (>=1) of the buy price to enter a limit sell order
- trade_type: currently only `LIMIT` is implemented
- order_duration: # of days before a limit order is cancelled
- order_amount_ratio: percentage (<=1) of the starting balance, or total current balance, whichever is less, that is used for the next order amount
- symbol: the stock symbol for the trading strategy, one of [QQQ, RITM]
- start_date: the start date for the back testing
- end_date: the end date for the back testing

### Historical pricing data properties
The historic pricing data is daily pricing information.  A historic price has specific features:
- symbol: one of [QQQ, RITM]
- date: the date of the daily price information
- open: the opening price
- high: the highest price on that day
- low: the lowest price on that day
- close: the price at the close of the day

## Install and run
Dependencies are managed using Poetry

### Python version
3.11

### Install
From the terminal, run: `make install`

### Run
From the terminal, run: `make run`

### Test
From the terminal, run: `make test`
