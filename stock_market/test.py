from stock_market.market_data.b3 import IntraDayPriceB3

initialization = IntraDayPriceB3(date='2020-07-16')
df = initialization.get_data(ticker='PETR4')
