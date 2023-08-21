import os
import csv
import time
from .objects import Price, Balance
from decimal import Decimal


class Dao:
    def __init__(self):
        self.now = str(int(time.time()))
        print('now:', self.now)

    @staticmethod
    def get_all_symbols() -> set:
        symbols = set()
        for file in os.listdir('algofin/pricing_data'):
            if file.endswith(".csv"):
                symbols.add(file[0:-4])
        print('symbols:', symbols)
        return symbols

    def load_all_pricing_data(self) -> dict:
        pricing_data = dict()
        for symbol in self.get_all_symbols():
            pricing_data[symbol] = self.get_prices(symbol)
        return pricing_data

    @staticmethod
    def create_folder_(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def write_to_csv(self, name: str, rows: list):
        path = 'algofin/results/' + self.now
        self.create_folder_(path)
        fullpath = path + '/' + name + '.csv'
        print('writing rows to csv:', fullpath)
        with open(fullpath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    @staticmethod
    def load_balance(row):
        print('row', row)
        return Balance(int(row[0]), row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), int(row[5]))

    @staticmethod
    def load_price(row):
        return Price(row[0], row[1], Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), Decimal(row[5]))

    @staticmethod
    def read_csv(path, load_object, skip_headers=False):
        print('reading csv:', path)

        with open(path, newline='') as f:
            reader = csv.reader(f)
            if skip_headers:
                next(reader)  # discarded, used to skip the first row of headers to cast to floats on the following rows
            data = [load_object(row) for row in reader]
            print(data[:10])
        return data

    def get_prices(self, name):
        path = 'algofin/pricing_data/' + name + '.csv'
        return self.read_csv(path, self.load_price, True)

    def get_balances(self):
        path = 'algofin/results/' + self.now + '/balances.csv'
        return self.read_csv(path, self.load_balance, False)
