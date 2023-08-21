from datetime import date
from strategies import Strategy, Strategies, LIMIT, MARKET
from dao import Dao
from objects import Balance, Order, Price, Trade
from collections import defaultdict
from decimal import Decimal

# specify constants
BUY = 'buy'
SELL = 'sell'


class BackTest:
    def __init__(self, starting_balance: int = 10000):
        """
        Initializes the BackTest class so that strategies can be back tested against historical daily
        pricing information.

        Parameters
        ----------
        starting_balance : int
            The starting balance for back testing

        Returns
        -------
        BackTest
        """
        self.dao = Dao()
        self.symbols = self.dao.get_all_symbols()
        self.pricing_data = self.dao.load_all_pricing_data()
        self.starting_balance = Decimal(starting_balance)
        self.strategies = Strategies.get_strategies()
        self.order_id_offset = 0
        self.trade_id_offset = 0

    def implement_all_hard_coded_strategies(self):
        """
        Iterates over hard coded sample strategies and back tests them against historical daily
        pricing information.  Stores the results information in the ../results folder partitioned by class init time.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for strategy in self.strategies:
            self.implement_(strategy)

    def get_max_strategy_ending_balance(self) -> (int, Decimal, Balance):
        """
        Iterates over all of the results information in the ../results folder from this class init time and finds
        the strategy that produced the largest ending balance.

        Parameters
        ----------
        None

        Returns
        -------
        (int, Decimal, Balance)
            The strategy ID that produced the largest ending balance
            The largest ending balance amount
            The largest ending Balance record
        """
        ending_balances, max_balance_of_each_strategy = self._get_strategy_ending_and_max_balances()
        strategy_id = 0
        ending_balance = 0
        balance = None
        for k, v in ending_balances.items():
            if v[0] > ending_balance:
                strategy_id = k
                ending_balance = v[0]
                balance = v[1]
        return strategy_id, ending_balance, balance

    def get_max_strategy_balance_at_anytime(self):
        """
        Iterates over all of the results information in the ../results folder from this class init time and finds
        the strategy that produced the largest balance at any time during the back testing period.

        Parameters
        ----------
        None

        Returns
        -------
        (int, Decimal, Balance)
            The strategy ID that produced the largest anytime balance
            The largest anytime balance amount
            The largest anytime Balance record
        """
        ending_balances, max_balance_of_each_strategy = self._get_strategy_ending_and_max_balances()
        strategy_id = 0
        anytime_balance = Decimal(0)
        balance = None
        for k, v in max_balance_of_each_strategy.items():
            if v[0] > anytime_balance:
                strategy_id = k
                anytime_balance = v[0]
                balance = v[1]
        return strategy_id, anytime_balance, balance

    def _get_strategy_ending_and_max_balances(self):
        ending_balances = dict()
        max_balance_of_each_strategy = defaultdict(tuple)
        balances = self.dao.get_balances()
        for balance in balances:
            total_balance = balance[2] + balance[3] + balance[4]
            ending_balances[balance[0]] = (total_balance, balance)
            if total_balance > max_balance_of_each_strategy.get(balance[0], (Decimal(0), None))[0]:
                max_balance_of_each_strategy[balance[0]] = (total_balance, balance)
        return ending_balances, max_balance_of_each_strategy

    def _get_starting_trading_day(self, prices, start_date):
        strategy_is_live = False
        trading_day = 0
        for day in prices:
            if self._greater_than_or_equal(day.date, start_date):
                strategy_is_live = True
                break
            trading_day += 1
        return strategy_is_live, trading_day

    def implement_(self, strategy: Strategy):
        """
        Implements a strategy against historic daily pricing info during the time period specified for the strategy.
        Saves the results in the ../results folder from this class init time.

        Parameters
        ----------
        strategy
            The strategy that is being implemented

        Returns
        -------
        None
        """
        self.dao._write_to_csv('strategies', [strategy])
        starting_balance = Balance(strategy_id=strategy.strategy_id, date=strategy.start_date,
                                   cash_balance=self.starting_balance,
                                   order_balance=Decimal(0), invested_balance=Decimal(0), number_of_shares=0)
        orders = []
        trades = []
        balances = [starting_balance]

        prices = self.pricing_data[strategy.symbol]

        strategy_is_live, trading_day = self._get_starting_trading_day(prices, strategy.start_date)

        while strategy_is_live:
            price = prices[trading_day]

            # check for sells that were executed
            orders, trades, balances = self._process_executed_sell_orders(orders, trades, balances, strategy, price)

            # check for buys that were executed
            orders, trades, balances = self._process_executed_buy_orders(orders, trades, balances, strategy,
                                                                         trading_day,
                                                                         prices)

            # check for sells that expired
            orders = self._change_expired_sell_orders_to_maket_orders(orders, price)

            # check for buys that expired
            orders, balances = self._close_expired_buy_orders(orders, balances, strategy, price)

            # enter new buy order
            orders, balances = self._add_new_buy_order(orders, balances, strategy, trading_day, prices)

            trading_day += 1
            if self._greater_than_or_equal(price.date, strategy.end_date):
                strategy_is_live = False
                order_balance, cash_balance, invested_balance, balance_num_of_shares = self._get_current_balances(
                    balances, price)
                last_balance = Balance(strategy_id=strategy.strategy_id,
                                       date=price.date,
                                       order_balance=order_balance,
                                       cash_balance=cash_balance,
                                       invested_balance=self._total_(balance_num_of_shares, price.close),
                                       number_of_shares=balance_num_of_shares)
                balances.append(last_balance)
                self.order_id_offset += len(orders)
                self.trade_id_offset += len(trades)

        self.dao._write_to_csv('orders', orders)
        self.dao._write_to_csv('trades', trades)
        self.dao._write_to_csv('balances', balances)

    def _process_executed_buy_orders(self, orders: [Order], trades: [Trade], balances: [Balance], strategy: Strategy,
                                     trading_day: int, prices: [Price]) -> ([Order], [Trade], [Balance]):

        price = prices[trading_day]
        order_balance, cash_balance, invested_balance, balance_num_of_shares = self._get_current_balances(balances,
                                                                                                          price)
        for past_order in orders:
            # check active buys
            if past_order.active and past_order.buy_sell == BUY and self._greater_than_or_equal(past_order.close_date,
                                                                                                price.date):
                # check buy price condition was met
                if past_order.price >= min(price.open, price.low, price.close):

                    buy_price = past_order.price
                    if buy_price > price.open:
                        buy_price = price.open

                    buy_total = self._total_(past_order.number_of_shares, buy_price)
                    new_num_of_shares = balance_num_of_shares + past_order.number_of_shares

                    balance = Balance(strategy_id=strategy.strategy_id,
                                      date=price.date,
                                      order_balance=order_balance - past_order.total,
                                      cash_balance=cash_balance + past_order.total - buy_total,
                                      invested_balance=self._total_(new_num_of_shares, price.close),
                                      number_of_shares=new_num_of_shares)
                    balances.append(balance)
                    past_order.active = False

                    trade = Trade(trade_id=len(trades) + 1 + self.trade_id_offset,
                                  order_id=past_order.order_id,
                                  number_of_shares=past_order.number_of_shares,
                                  date=price.date,
                                  price=buy_price,
                                  total=buy_total)
                    trades.append(trade)

                    sale_price = buy_price * strategy.sell_offset
                    sale_total = self._total_(past_order.number_of_shares, sale_price)
                    sale_order = Order(order_id=len(orders) + 1 + self.order_id_offset,
                                       strategy_id=strategy.strategy_id,
                                       symbol=strategy.symbol,
                                       number_of_shares=past_order.number_of_shares,
                                       buy_sell=SELL,
                                       trade_type=LIMIT,
                                       open_date=prices[trading_day + 1].date,
                                       close_date=prices[
                                           min(trading_day + 1 + strategy.order_duration, len(prices) - 1)].date,
                                       price=sale_price,
                                       total=sale_total,
                                       active=True)
                    orders.append(sale_order)

        return orders, trades, balances

    def _process_executed_sell_orders(self, orders: [Order], trades: [Trade], balances: [Balance], strategy: Strategy,
                                      price: Price) -> ([Order], [Trade], [Balance]):

        order_balance, cash_balance, invested_balance, balance_num_of_shares = self._get_current_balances(balances,
                                                                                                          price)
        # we should not have to check all past orders, can we check just the last one? What happens
        # during the first and last order duration?
        for past_order in orders:
            # check if past sell orders have executed today
            # check for active market sales
            if past_order.active and past_order.buy_sell == SELL and past_order.trade_type == MARKET:

                sale_total = self._total_(past_order.number_of_shares, price.open)
                new_num_shares = past_order.number_of_shares + balance_num_of_shares

                trade = Trade(trade_id=len(trades) + 1 + self.trade_id_offset,
                              order_id=past_order.order_id,
                              number_of_shares=past_order.number_of_shares,
                              date=price.date,
                              price=price.open,
                              total=sale_total)
                trades.append(trade)

                balance = Balance(strategy_id=strategy.strategy_id,
                                  date=price.date,
                                  order_balance=order_balance,
                                  cash_balance=cash_balance + sale_total,
                                  invested_balance=self._total_(new_num_shares, price.close),
                                  number_of_shares=new_num_shares)
                balances.append(balance)

                past_order.active = False

            # check active limit sales
            elif past_order.active and past_order.buy_sell == SELL and past_order.trade_type == LIMIT and self._greater_than_or_equal(
                    past_order.close_date,
                    price.date):
                # check sale price conditions were met
                if past_order.price <= max(price.open, price.high, price.close):
                    sale_price = past_order.price
                    if sale_price < price.open:
                        sale_price = price.open

                    sale_total = self._total_(past_order.number_of_shares, sale_price)
                    new_num_of_shares = balance_num_of_shares - past_order.number_of_shares

                    balance = Balance(strategy_id=strategy.strategy_id,
                                      date=price.date,
                                      order_balance=order_balance,
                                      cash_balance=cash_balance + sale_total,
                                      invested_balance=self._total_(new_num_of_shares, price.close),
                                      number_of_shares=new_num_of_shares)
                    balances.append(balance)
                    past_order.active = False

                    trade = Trade(trade_id=len(trades) + 1 + self.trade_id_offset,
                                  order_id=past_order.order_id,
                                  number_of_shares=past_order.number_of_shares,
                                  date=price.date,
                                  price=sale_price,
                                  total=sale_total)
                    trades.append(trade)

        return orders, trades, balances

    @staticmethod
    def _total_(num_shares: int, current_price: float):
        return num_shares * current_price

    def _add_new_buy_order(self, orders: [Order], balances: [Balance], strategy: Strategy, trading_day: int,
                           prices) -> (
            [Order], [Balance]):

        price = prices[trading_day]

        order_balance, cash_balance, invested_balance, balance_num_of_shares = self._get_current_balances(balances,
                                                                                                          price)

        default_order_amount = self.starting_balance * strategy.order_amount_ratio

        if cash_balance > Decimal(0):
            # create_order
            order_amount = default_order_amount if default_order_amount < cash_balance else cash_balance
            buy_offset_price = price.close * strategy.buy_offset
            order_num_of_shares = int(order_amount / buy_offset_price)
            if order_num_of_shares > 0:
                open_date = prices[trading_day + 1].date
                close = prices[min(trading_day + 1 + strategy.order_duration, len(prices) - 1)].date
                total = buy_offset_price * order_num_of_shares
                order = Order(order_id=len(orders) + 1 + self.order_id_offset,
                              strategy_id=strategy.strategy_id,
                              symbol=strategy.symbol,
                              number_of_shares=order_num_of_shares,
                              buy_sell=BUY,
                              trade_type='limit',
                              open_date=open_date,
                              close_date=close,
                              price=buy_offset_price,
                              total=total,
                              active=True)
                orders.append(order)
                cash_balance -= total
                order_balance += total
                # update the balance
                balance = Balance(strategy.strategy_id, open_date, order_balance, cash_balance, invested_balance,
                                  balance_num_of_shares)
                balances.append(balance)

        return orders, balances

    def _change_expired_sell_orders_to_maket_orders(self, orders: [Order], price: Price) -> (
            [Order], [Trade], [Balance]):

        for past_order in orders:
            # check if past sells have expired
            if past_order.active and past_order.buy_sell == SELL and self._less_than_or_equal(past_order.close_date,
                                                                                              price.date):
                # convert the sale to a market sell at the next opening price
                past_order.trade_type = MARKET

        return orders

    def _close_expired_buy_orders(self, orders: [Order], balances: [Balance], strategy: Strategy, price: Price) -> (
            [Order], [Balance]):

        order_balance, cash_balance, invested_balance, balance_num_of_shares = self._get_current_balances(balances,
                                                                                                          price)

        # we should not have to check all past orders, can we check just the last one? What happens
        # during the first and last order duration? such as for past_order in orders[-(strategy.order_duration + 1):]:
        for past_order in orders:
            # check if past buys have expired
            if past_order.active and past_order.buy_sell == BUY and self._less_than_or_equal(past_order.close_date,
                                                                                             price.date):
                order_balance -= past_order.total
                cash_balance += past_order.total
                balance = Balance(strategy_id=strategy.strategy_id,
                                  date=price.date,
                                  order_balance=order_balance,
                                  cash_balance=cash_balance,
                                  invested_balance=invested_balance,
                                  number_of_shares=balance_num_of_shares)
                balances.append(balance)
                past_order.active = False

        return orders, balances

    def _get_current_balances(self, balances: [Balance], price: Price):
        order_balance = balances[-1].order_balance
        cash_balance = balances[-1].cash_balance
        balance_num_of_shares = balances[-1].number_of_shares
        invested_balance = balance_num_of_shares * price.close
        return order_balance, cash_balance, invested_balance, balance_num_of_shares

    @staticmethod
    def _equal(left: str, right: str):
        return date.fromisoformat(left) == date.fromisoformat(right)

    @staticmethod
    def _less_than_or_equal(left: str, right: str):
        return date.fromisoformat(left) <= date.fromisoformat(right)

    @staticmethod
    def _greater_than_or_equal(left: str, right: str):
        return date.fromisoformat(left) >= date.fromisoformat(right)


if __name__ == '__main__':
    back_test = BackTest()
    back_test.implement_all_hard_coded_strategies()
    strategy_id, ending_balance, balance = back_test.get_max_strategy_ending_balance()
    best_hard_coded_strategy = back_test.dao.get_strategy(strategy_id)
    print(strategy_id, ending_balance, balance, best_hard_coded_strategy)
