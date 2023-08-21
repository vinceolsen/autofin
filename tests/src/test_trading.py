from ...algofin.src.trading import BackTest
from ...algofin.src.objects import Balance


def test_it_finds_the_strategy_with_max_ending_balance():
    back_test = BackTest()
    back_test.implement_all_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_ending_balance()
    assert strategy_id == 1
    assert round(ending_balance, 2) == 245631.99
    assert balance == Balance(strategy_id=1, date='2023-05-01', order_balance=9599.931128899996, cash_balance=188.97569011500232, invested_balance=235843.081464, number_of_shares=732)


def test_it_finds_the_strategy_with_max_balance_at_anytime():
    back_test = BackTest()
    back_test.implement_all_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_balance_at_anytime()
    assert strategy_id == 1
    assert round(ending_balance, 2) == 245631.99
    assert balance == Balance(strategy_id=1, date='2023-05-01', order_balance=9599.931128899996, cash_balance=188.97569011500232, invested_balance=235843.081464, number_of_shares=732)
