from ...algofin.src.trading_strategies import BackTest


def test_true():
    assert True

def test_it_runs_everything():
    trading_strategies = BackTest()
    assert True

def test_it_gets_all_symbols():
    symbols = BackTest().symbols
    assert symbols == {'QQQ', 'RITM'}

def test_it_loads_all_pricing_data():
    pricing_data = BackTest().pricing_data
    assert len(pricing_data) == 2


