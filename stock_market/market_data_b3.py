import requests
import pandas as pd
import numpy as np

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


class IntraDayPriceB3:

    def __init__(self,  date, stock=True, derivative=None):
        # format date  YYYY-MM-DD
        self.stock = stock
        self.derivative = derivative
        self.date = date
        self.url = 'https://arquivos.b3.com.br/apinegocios/tickercsv/{}'

        self.df = None

        self._load_data()

    def _load_data(self):
        try:
            self.url = self.url.format(self.date)
            _data = urlopen(self.url)
            _zipfile = ZipFile(BytesIO(_data.read()))

            with _zipfile.open(_zipfile.namelist()[0], 'r') as g:
                self.df = pd.read_csv(g, sep=';')

            if self.stock:
                self.df = self.df[(self.df .TckrSymb.str.len() == 5)]
            return self.df
        except ValueError:
            print(
                "There is a date range limit of two weeks. After that the data is not acessible")

    def get_data(self, ticker):
        data = self.df[["RptDt", "TckrSymb", "GrssTradAmt",
                        "TradQty", "NtryTm", "TradId", "TradDt"]]
        data.columns = ["report_date", "ticker", "price",
                        "trade_quatity", "entry_time", "trade_id", "trade_date"]
        data['price'] = (
            data['price'].str.replace(',', '.')).astype(float)

        return data[data["ticker"] == ticker]
