from ...algofin.src.strategies import Strategies


def test_get_all_strategies_gets_correct_number():
    strategies = Strategies.get_strategies()
    assert len(strategies) == 8
