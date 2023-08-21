from .objects import Strategy
from decimal import Decimal

# specify constants
LIMIT = 'limit'
MARKET = 'market'
QQQ = 'QQQ'
RITM = 'RITM'
QQQ_start = '1999-05-01'
QQQ_end = '2023-05-01'
RITM_start = '1999-05-01'
RITM_end = '2023-05-01'


class Strategies:
    def __init__(self):
        pass

    @staticmethod
    def get_strategies():
        strategies = []

        buy_and_hold_name = 'buy and hold'
        buy_and_hold_description = 'buy on start date and hold until end date'
        buy_low_sell_high_name = 'limit buy offset down; limit sell offset up'
        buy_low_sell_high_description = 'Set a limit buy at current price * buy offset; when that purchase is made; set a limit sell at purchase price * sell offset. The purchase order expires after the specified duration of trading days if not fulfilled.'
        strategy_id = 0

        qqq5down10up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                     strategy_name=buy_low_sell_high_name,
                                     description=buy_low_sell_high_description,
                                     buy_offset=Decimal('0.95'),
                                     sell_offset=Decimal('1.10'),
                                     trade_type=LIMIT,
                                     order_duration=10,
                                     order_amount_ratio=Decimal('0.1'),
                                     symbol=QQQ,
                                     start_date=QQQ_start,
                                     end_date=QQQ_end)
        strategies.append(qqq5down10up10day)

        qqq3down6up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                    strategy_name=buy_low_sell_high_name,
                                    description=buy_low_sell_high_description,
                                    buy_offset=Decimal('0.97'),
                                    sell_offset=Decimal('1.06'),
                                    trade_type=LIMIT,
                                    order_duration=10,
                                    order_amount_ratio=Decimal('0.1'),
                                    symbol=QQQ,
                                    start_date=QQQ_start,
                                    end_date=QQQ_end)
        strategies.append(qqq3down6up10day)

        qqq1down2up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                    strategy_name=buy_low_sell_high_name,
                                    description=buy_low_sell_high_description,
                                    buy_offset=Decimal('0.99'),
                                    sell_offset=Decimal('1.02'),
                                    trade_type=LIMIT,
                                    order_duration=10,
                                    order_amount_ratio=Decimal('0.1'),
                                    symbol=QQQ,
                                    start_date=QQQ_start,
                                    end_date=QQQ_end)
        strategies.append(qqq1down2up10day)

        ritm5down10up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                      strategy_name=buy_low_sell_high_name,
                                      description=buy_low_sell_high_description,
                                      buy_offset=Decimal('0.95'),
                                      sell_offset=Decimal('1.10'),
                                      trade_type=LIMIT,
                                      order_duration=10,
                                      order_amount_ratio=Decimal('0.1'),
                                      symbol=RITM,
                                      start_date=RITM_start,
                                      end_date=RITM_end)
        strategies.append(ritm5down10up10day)

        ritm3down6up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                     strategy_name=buy_low_sell_high_name,
                                     description=buy_low_sell_high_description,
                                     buy_offset=Decimal('0.97'),
                                     sell_offset=Decimal('1.06'),
                                     trade_type=LIMIT,
                                     order_duration=10,
                                     order_amount_ratio=Decimal('0.1'),
                                     symbol=RITM,
                                     start_date=RITM_start,
                                     end_date=RITM_end)
        strategies.append(ritm3down6up10day)

        ritm1down2up10day = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                     strategy_name=buy_low_sell_high_name,
                                     description=buy_low_sell_high_description,
                                     buy_offset=Decimal('0.99'),
                                     sell_offset=Decimal('1.02'),
                                     trade_type=LIMIT,
                                     order_duration=10,
                                     order_amount_ratio=Decimal('0.1'),
                                     symbol=RITM,
                                     start_date=RITM_start,
                                     end_date=RITM_end)
        strategies.append(ritm1down2up10day)

        qqq_buy_and_hold = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                    strategy_name=buy_and_hold_name,
                                    description=buy_and_hold_description,
                                    buy_offset=Decimal('1'),
                                    sell_offset=Decimal('1000'),
                                    trade_type=LIMIT,
                                    order_duration=100000,
                                    order_amount_ratio=Decimal('1'),
                                    symbol=QQQ,
                                    start_date=QQQ_start,
                                    end_date=QQQ_end)
        strategies.append(qqq_buy_and_hold)

        ritm_buy_and_hold = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                                     strategy_name=buy_and_hold_name,
                                     description=buy_and_hold_description,
                                     buy_offset=Decimal('1'),
                                     sell_offset=Decimal('1000'),
                                     trade_type=LIMIT,
                                     order_duration=100000,
                                     order_amount_ratio=Decimal('1'),
                                     symbol=RITM,
                                     start_date=RITM_start,
                                     end_date=RITM_end)
        strategies.append(ritm_buy_and_hold)

        return strategies
