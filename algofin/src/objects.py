from collections import namedtuple
from recordtype import recordtype


# specify objects
Price = namedtuple('Price', ['symbol', 'date', 'open', 'high', 'low', 'close'])


Order = recordtype('Order',
                   ['order_id', 'strategy_id', 'symbol', 'number_of_shares', 'buy_sell', 'trade_type',
                    'open_date', 'close_date', 'price', 'total', 'active'])


Trade = namedtuple('Trade', ['trade_id', 'order_id', 'number_of_shares', 'date', 'price', 'total'])


Balance = namedtuple('Balance',
                     ['strategy_id', 'date', 'order_balance', 'cash_balance', 'invested_balance', 'number_of_shares'])


Strategy = namedtuple('Strategy',
                      ['strategy_id', 'strategy_name', 'description', 'buy_offset', 'sell_offset', 'trade_type',
                       'order_duration', 'order_amount_ratio', 'symbol', 'start_date', 'end_date'])
