from collections import namedtuple
from recordtype import recordtype


# specify objects

Strategy = namedtuple('Strategy',
                      ['strategy_id', 'strategy_name', 'description', 'buy_offset', 'sell_offset', 'trade_type',
                       'order_duration', 'order_amount_ratio', 'symbol', 'start_date', 'end_date'])
"""
Strategy, an algorithm has specific features that can be configured.

Parameters
----------
- strategy_id: int, sequential
- strategy_name: string
- description: string
- buy_offset: at what percentage (<=1) of the current price to enter a limit buy order
- sell_offset: after a successful purchase, at what percentage (>=1) of the buy price to enter a limit sell order
- trade_type: currently only `LIMIT` is implemented
- order_duration: # of days before a limit order is cancelled
- order_amount_ratio: percentage (<=1) of the starting balance, or total current balance, whichever is less, that is used for the next order amount
- symbol: the stock symbol for the trading strategy, one of [QQQ, RITM]
- start_date: the start date for the back testing
- end_date: the end date for the back testing

Returns
-------
Strategy
    A strategy record
"""


Price = namedtuple('Price', ['symbol', 'date', 'open', 'high', 'low', 'close'])
"""
The historic pricing data is daily pricing information.  A historic price has specific features:

Parameters
----------
- symbol: one of [QQQ, RITM]
- date: the date of the daily price information
- open: the opening price
- high: the highest price on that day
- low: the lowest price on that day
- close: the price at the close of the day 

Returns
-------
Price
    A price record
"""


Order = recordtype('Order',
                   ['order_id', 'strategy_id', 'symbol', 'number_of_shares', 'buy_sell', 'trade_type',
                    'open_date', 'close_date', 'price', 'total', 'active'])
"""
Order record

Parameters
----------
- order_id: int, sequential
- strategy_id: which strategy is this order for
- symbol: which symbol is this order for
- number_of_shares: the integer number of shares
- buy_sell: one of ['buy', 'sell']
- trade_type: one of ['limit', 'market']
- open_date: the date the order was opened in string iso format: '2023-04-10'
- close_date: the date the order was closed in string iso format: '2023-04-17'
- price: the limit price of the order
- total: the total value of the order: number_of_shares * price
- active: whether the tade is active, one of [True, False]

Returns
-------
Order
    An order record
"""


Trade = namedtuple('Trade', ['trade_id', 'order_id', 'number_of_shares', 'date', 'price', 'total'])
"""
Trade record

Parameters
----------
- trade_id: int, sequential
- order_id: int, the id of the order that lead to this trade
- number_of_shares: the integer number of shares
- date: the date the trade was executed in string iso format: '2023-04-10'
- price: the price the trade was executed at
- total: the total value of the trade: number_of_shares * price

Returns
-------
Trade
    A trade record
"""


Balance = namedtuple('Balance',
                     ['strategy_id', 'date', 'order_balance', 'cash_balance', 'invested_balance', 'number_of_shares'])
"""
Balance record

Parameters
----------
- strategy_id: which strategy is this balance record for
- date: the date of the balance record in string iso format: '2023-04-10'
- order_balance: Decimal amount of the current balance that is devoted to outstanding orders.  
    The cash balance is reduced by the order amount to avoid a negative balance scenario.
- cash_balance: Decimal amount of cash
- invested_balance: Decimal amount of notional value of invested shares at the price at the time of this balance update
- number_of_shares: the integer number of shares owned

Returns
-------
Balance
    A balance record
"""
