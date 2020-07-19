import requests
import pandas as pd
import numpy as np
import datetime

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


class IntraDayPriceB3:
    def __init__(self,  date, stock=True, derivative=None):
        self.stock = stock
        self.derivative = derivative
        self.date = date
        self.url = 'https://arquivos.b3.com.br/apinegocios/tickercsv/{}'

        self.df = None

    def _load_data(self):
        self.url = self.url.format(self.date)
        _data = urlopen(self.url)
        _zipfile = ZipFile(BytesIO(_data.read()))

        with _zipfile.open(_zipfile.namelist()[0], 'r') as g:
            self.df = pd.read_csv(g, sep=';')

        if self.stock:
            self.df = self.df[(self.df .TckrSymb.str.len() == 5)]
        return self.df

    def get_data(self, ticker):
        self.df = self.df[["RptDt", "TckrSymb", "GrssTradAmt",
                           "TradQty", "NtryTm", "TradId", "TradDt"]]
        self.df.columns = ["report_date", "ticker", "price",
                           "trade_quatity", "entry_time", "trade_id", "trade_date"]
        self.df['price'] = (
            self.df['price'].str.replace(',', '.')).astype(float)

        self.df = self.df[self.df["ticker"] == ticker]
        return self.df
