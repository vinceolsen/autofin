from decimal import Decimal
from objects import Strategy
from strategies import LIMIT
from trading import BackTest


def find_optimal_strategy(start, end)-> Strategy:
    symbols = [
        'QQQ',
        # 'RITM'
    ]

    buy_offsets = [
        Decimal('0.90'),
        Decimal('0.91'),
        Decimal('0.92'),
        Decimal('0.93'),
        Decimal('0.94'),
        Decimal('0.95'),
        Decimal('0.96'),
        Decimal('0.97'),
        Decimal('0.98'),
        Decimal('0.99'),
    ]

    sell_offsets = [
        Decimal('1.01'),
        Decimal('1.02'),
        Decimal('1.03'),
        Decimal('1.04'),
        Decimal('1.05'),
        Decimal('1.06'),
        Decimal('1.07'),
        Decimal('1.08'),
        Decimal('1.09'),
        Decimal('1.10'),
    ]

    order_amount_ratios = [
        Decimal('0.05'),
        Decimal('0.10'),
        Decimal('0.15'),
        Decimal('0.20')
    ]

    strategy_id = 1

    back_test = BackTest()

    for symbol in symbols:
        for order_amount_ratio in order_amount_ratios:
            for buy_offset in buy_offsets:
                for sell_offset in sell_offsets:
                    strategy = Strategy(strategy_id=(strategy_id := strategy_id + 1),
                             strategy_name='limit buy offset down; limit sell offset up',
                             description='Set a limit buy at current price * buy offset; when that purchase is made; set a limit sell at purchase price * sell offset. The purchase order expires after the specified duration of trading days if not fulfilled.',
                             buy_offset=buy_offset,
                             sell_offset=sell_offset,
                             trade_type=LIMIT,
                             order_duration=10,
                             order_amount_ratio=order_amount_ratio,
                             symbol=symbol,
                             start_date=start,
                             end_date=end)

                    back_test.implement_(strategy)

    anytime_strategy_id, anytime_balance_amount, anytime_balance = back_test.get_max_strategy_balance_at_anytime()
    anytime_strategy = back_test.dao.get_strategy(anytime_strategy_id)
    print('Max balance anytime:', anytime_strategy_id, anytime_balance_amount, anytime_balance)
    print(anytime_strategy)

    ending_strategy_id, ending_balance_amount, ending_balance = back_test.get_max_strategy_ending_balance()
    ending_strategy = back_test.dao.get_strategy(ending_strategy_id)
    print('Max ending balance:', ending_strategy_id, ending_balance_amount, ending_balance)
    print(ending_strategy)

    return ending_strategy


if __name__ == '__main__':
    best_strategy = find_optimal_strategy('2005-01-01','2016-01-01')
    print('\n\nBest strategy:', best_strategy)
