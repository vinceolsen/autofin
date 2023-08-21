from ..algofin.src.dao import Dao, Price
from decimal import Decimal
from ..algofin.src.objects import Strategy


def test_it_gets_all_symbols():
    symbols = Dao().get_all_symbols()
    assert symbols == {'QQQ', 'RITM'}


def test_it_loads_a_pricing_file():
    prices = Dao()._get_prices('RITM')
    assert len(prices) == 2544
    assert len(prices[0]) == 6
    assert prices[0] == Price(symbol='RITM', date='2013-05-02', open=Decimal('14.0'), high=Decimal('14.0'), low=Decimal('13.0'), close=Decimal('13.52'))
    assert prices[-1] == Price(symbol='RITM', date='2023-06-08', open=Decimal('8.88'), high=Decimal('8.96'), low=Decimal('8.81'), close=Decimal('8.92'))


def test_it_loads_all_pricing_data():
    pricing_data = Dao().load_all_pricing_data()
    assert len(pricing_data) == 2

def test_it_loads_strategies():
    dao = Dao()
    strategies = []
    qqq5down10up10day = Strategy(strategy_id=1,
                                     strategy_name="buy_low_sell_high_name",
                                     description="buy_low_sell_high_description",
                                     buy_offset=Decimal('0.95'),
                                     sell_offset=Decimal('1.10'),
                                     trade_type="LIMIT",
                                     order_duration=10,
                                     order_amount_ratio=Decimal('0.1'),
                                     symbol="QQQ",
                                     start_date='QQQ_start',
                                     end_date='QQQ_end')
    strategies.append(qqq5down10up10day)

    qqq3down6up10day = Strategy(strategy_id=2,
                                    strategy_name='buy_low_sell_high_name',
                                    description='buy_low_sell_high_description',
                                    buy_offset=Decimal('0.97'),
                                    sell_offset=Decimal('1.06'),
                                    trade_type='LIMIT',
                                    order_duration=10,
                                    order_amount_ratio=Decimal('0.1'),
                                    symbol='QQQ',
                                    start_date='QQQ_start',
                                    end_date='QQQ_end')
    strategies.append(qqq3down6up10day)
    dao._write_to_csv('strategies', strategies)
    read_strategies = dao.get_strategies()
    assert len(read_strategies) == 2
    assert strategies == read_strategies

    specific_strategy = dao.get_strategy(2)
    assert specific_strategy == qqq3down6up10day

