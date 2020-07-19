import requests
import pandas as pd
import numpy as np

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


class IntraDayPriceB3:
    def __init__(self,  date, stock=None, derivative=None):
        self.stock = stock
        self.derivative = derivative
        self.date = date
        self.url = 'https://arquivos.b3.com.br/apinegocios/tickercsv/{}'

    def _load_data(self):
        self.url = self.url.format(self.date)
        _data = urlopen(self.url)
        _zipfile = ZipFile(BytesIO(_data.read()))

        with _zipfile.open(_zipfile.namelist()[0], 'r') as g:
            df = pd.read_csv(g, sep=';')

        return df
