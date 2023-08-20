import os
import csv
from collections import namedtuple
import time


# specify objects
Price = namedtuple('Price', ['symbol', 'date', 'open', 'high', 'low', 'close'])


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
            pricing_data[symbol] = self.load_csv(symbol)
        return pricing_data

    @staticmethod
    def load_csv(name):
        fullpath = 'algofin/pricing_data/' + name + '.csv'
        print('reading csv:', fullpath)

        with open(fullpath, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # discarded, used to skip the first row to cast to floats on the following rows
            data = [Price(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5])) for row in reader]
            print(data[:10])
        return data

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
