import datetime
import os
import sys
import numpy as np
import talib
from time import sleep
from numpy import interp


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

msec = 1000
minute = 60 * msec
hold = 30


import ccxt

gdax = ccxt.gdax({
    'rateLimit': 3000,
    'enableRateLimit': True,
    #'verbose': True,
})
bitfinex = ccxt.bitfinex({
    'rateLimit': 3000,
    'enableRateLimit': True,
    #'verbose': True,
})

kraken = ccxt.kraken({
    'rateLimit': 3000,
    'enableRateLimit': True,
    #'verbose': True,
})

gdax_currency = ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'BTC/GBP', 'LTC/USD', 'LTC/EUR', 'LTC/BTC', 'BCH/USD','BCH/EUR','BCH/BTC']

bitfinex_currency = ['ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD',  'LTC/BTC', 'BCH/USD','BCH/BTC', 'XRP/USD','XRP/BTC','EOS/USD','EOS/BTC', 'EOS/ETH','BCH/ETH','IOTA/EUR','IOTA/USD','IOTA/BTC','IOTA/ETH','NEO/USD','NEO/BTC','NEO/ETH','DASH/BTC','ELF/USD','OMG/USD','BTG/USD','SAN/USD','QTUM/USD','ETP/USD','TRX/USD','ZRX/USD','BAT/USD']

kraken_currency = ['ETH/EUR','ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD',  'LTC/BTC', 'LTC/EUR', 'BCH/USD', 'BCH/EUR','BCH/BTC', 'XRP/USD', 'XRP/EUR','XRP/BTC','EOS/BTC', 'EOS/ETH','DASH/BTC','DASH/EUR','XMR/EUR','REP/ETH','REP/EUR','REP/BTC','XMR/USD','ETC/USD','ETC/EUR','DASH/USD','ETC/BTC','ZEC/BTC'
                   ,'BTC/CAD','ZEC/USD','ZEC/EUR','ETH/CAD','XLM/BTC','XDG/BTC','MLN/BTC','ICN/ETH','ICN/BTC','GNO/BTC','GNO/ETH']


def update(currency,exchange,period):
    try:
        start_date = datetime.date.today() + datetime.timedelta(-60)
        start_date2 = str(start_date) + " 00:00:00"
        from_timestamp = exchange.parse8601(start_date2)
        update.current_closing = exchange.fetch_ticker(currency)['last']
        update.raw_data = exchange.fetch_ohlcv(currency, period, from_timestamp)
        sleep(0.035)
    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        sleep(0.035)
    return update.raw_data


def bband():
    try:
        cleandata = []
        for x in xrange(60):
            cleandata.append(update.raw_data[x][4])
        reverse_data_list = cleandata[::-1]
        raw_input_array = np.array(reverse_data_list)
        upperband, middleband, lowerband = talib.BBANDS(raw_input_array, 20, 2, 2, 0)
        upperband_last = upperband[-1]
        middleband_last = middleband[-1]
        lowerband_last = lowerband[-1]
        bbands_fraction = (update.current_closing-lowerband_last)/(upperband_last-lowerband_last)

    except:
        sleep(0.035)
    return update.current_closing, bbands_fraction, upperband_last,middleband_last, lowerband_last



def bband_1h(exchange, currency):
    try:
        for x in currency:
            update(x,exchange,'1h')
            output = interp(bband()[1], [-25, 25], [0, 1])
            print(x,output)
    except:
        print("error")
    return output

def bband_1d(exchange, currency):
    try:
        for x in currency:
            update(x,exchange,'1d')
            output = interp(bband()[1], [-2, 2], [0, 1])
            print(x,output)

    except:
        print("error")
    return output

def MACD(exchange,currency):
    try:
        for x in currency:
            update(x,exchange,'1d')
            cleandata = []
            print(x)
            for x in xrange(60):
                cleandata.append(update.raw_data[x][4])
            reverse_data_list = cleandata[::-1]
            raw_input_array = np.array(reverse_data_list)
            macd, macdsignal, macdhist = talib.MACD(raw_input_array, fastperiod = 12, slowperiod = 26, signalperiod = 9)
            print(macd[-1], macdsignal[-1], macdhist[-1])
    except:
        print("error")
    return macd, macdsignal, macdhist

MACD(gdax,gdax_currency)
