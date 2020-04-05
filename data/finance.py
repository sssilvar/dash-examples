import datetime
from dateutil.relativedelta import relativedelta

from pandas_datareader import get_iex_symbols
import pandas_datareader.data as pdr

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()


def get_stock_data(stock='GE'):
    return pdr.get_data_yahoo(stock,
                              start=start,
                              end=end)


def get_dropdown_options():
    symbols = get_iex_symbols()
    symbols = symbols.query('isEnabled == True')

    options = symbols[['symbol', 'name']]
    options['label'] = options['name'] + ' (' + options['symbol'] + ')'
    options['value'] = options['symbol']

    return options[['label', 'value']].to_dict('records')
