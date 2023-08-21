from decimal import Decimal
from ...algofin.src.trading import BackTest
from ...algofin.src.objects import Balance


def test_it_finds_the_strategy_with_max_ending_balance():
    back_test = BackTest()
    back_test.implement_all_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_ending_balance()
    assert strategy_id == 1
    assert ending_balance.quantize(Decimal('.000001')) == Decimal('245631.988283')
    assert balance == Balance(strategy_id=1, date='2023-05-01', order_balance=Decimal('9599.93112890'),
                              cash_balance=Decimal('188.9756901150'), invested_balance=Decimal('235843.081464'),
                              number_of_shares=732)


def test_it_finds_the_strategy_with_max_balance_at_anytime():
    back_test = BackTest()
    back_test.implement_all_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_balance_at_anytime()
    assert strategy_id == 1
    assert ending_balance.quantize(Decimal('.000001')) == Decimal('245631.988283')
    assert balance == Balance(strategy_id=1, date='2023-05-01', order_balance=Decimal('9599.93112890'),
                              cash_balance=Decimal('188.9756901150'), invested_balance=Decimal('235843.081464'),
                              number_of_shares=732)
