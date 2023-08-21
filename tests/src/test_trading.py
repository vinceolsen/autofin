from ...algofin.src.trading import BackTest


def test_true():
    assert True


def test_it_finds_the_strategy_with_max_ending_balance():
    back_test = BackTest()
    back_test.implement_all_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_ending_balance()
    assert strategy_id == 1
    assert round(ending_balance, 2) == 245631.99
