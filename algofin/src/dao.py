import os
import csv
import time
from objects import Price, Balance, Strategy
from decimal import Decimal


class Dao:
    def __init__(self):
        self.now = str(int(time.time()))
        print('now:', self.now)

    @staticmethod
    def get_all_symbols() -> set:
        """
        Gets the symbols of all the pricing data based on the file names in the ../pricing_data folder

        Parameters
        ----------
        None

        Returns
        -------
        {String}
            Set of stock symbols
        """
        symbols = set()
        for file in os.listdir('algofin/pricing_data'):
            if file.endswith(".csv"):
                symbols.add(file[0:-4])
        print('symbols:', symbols)
        return symbols

    def load_all_pricing_data(self) -> dict:
        """
        Gets all the pricing data based on the files in the ../pricing_data folder

        Parameters
        ----------
        None

        Returns
        -------
        [Price]
            List of daily stock prices
        """
        pricing_data = dict()
        for symbol in self.get_all_symbols():
            pricing_data[symbol] = self._get_prices(symbol)
        return pricing_data

    @staticmethod
    def _create_folder_(path) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    def _write_to_csv(self, name: str, rows: list) -> None:
        path = 'algofin/results/' + self.now
        self._create_folder_(path)
        fullpath = path + '/' + name + '.csv'
        print('writing rows to csv:', fullpath)
        with open(fullpath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    @staticmethod
    def load_balance(row) -> Balance:
        return Balance(int(row[0]), row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), int(row[5]))

    @staticmethod
    def load_price(row) -> Price:
        return Price(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), Decimal(row[5]))

    @staticmethod
    def load_strategy(row) -> Strategy:
        return Strategy(int(row[0]), row[1], row[2], Decimal(row[3]), Decimal(row[4]), row[5], int(row[6]),
                        Decimal(row[7]), row[8], row[9], row[10])

    @staticmethod
    def _read_csv(path, load_object, skip_headers=False) -> []:
        print('reading csv:', path)

        with open(path, newline='') as f:
            reader = csv.reader(f)
            if skip_headers:
                next(reader)  # discarded, used to skip the first row of headers to cast to specific types on the following rows
            data = [load_object(row) for row in reader]
            print(data[:10])
        return data

    def _get_prices(self, name) -> [Price]:
        path = 'algofin/pricing_data/' + name + '.csv'
        return self._read_csv(path, self.load_price, True)

    def get_balances(self) -> [Balance]:
        """
        Gets all the balance records from this init time of BackTest class

        Parameters
        ----------
        None

        Returns
        -------
        [Balance]
            List of balance records
        """
        path = 'algofin/results/' + self.now + '/balances.csv'
        return self._read_csv(path, self.load_balance, False)

    def get_strategies(self) -> [Strategy]:
        """
        Gets all the strategy records from this init time of BackTest class

        Parameters
        ----------
        None

        Returns
        -------
        [strategy]
            List of strategy records
        """
        path = 'algofin/results/' + self.now + '/strategies.csv'
        return self._read_csv(path, self.load_strategy, False)

    def get_strategy(self, id: int) -> Strategy:
        """
        Gets a specific strategy record from this init time of BackTest class

        Parameters
        ----------
        id
            The strategy id

        Returns
        -------
        strategy
            A strategy record
        """
        strategies = self.get_strategies()
        for strategy in strategies:
            if strategy[0] == id:
                return strategy
