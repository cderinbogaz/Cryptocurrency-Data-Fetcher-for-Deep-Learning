# coding=utf-8
import datetime
import os
import sys
import dataset
import ccxt
from time import sleep
import requests
import json
import ssl
import xmltodict
import urllib2
import time

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

msec = 1000
minute = 60 * msec
hold = 30
exchange_dict = {

    'gdax': ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'BTC/GBP', 'LTC/USD', 'LTC/EUR', 'LTC/BTC',
             'BCH/USD', 'BCH/EUR', 'BCH/BTC'],

    'bitfinex': ['ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'BCH/USD', 'BCH/BTC', 'XRP/USD',
                 'XRP/BTC', 'EOS/USD', 'EOS/BTC', 'EOS/ETH', 'BCH/ETH', 'IOTA/EUR', 'IOTA/USD', 'IOTA/BTC', 'IOTA/ETH',
                 'NEO/USD', 'NEO/BTC', 'NEO/ETH', 'DASH/BTC', 'ELF/USD', 'OMG/USD', 'BTG/USD', 'SAN/USD', 'QTUM/USD',
                 'ETP/USD', 'TRX/USD', 'ZRX/USD', 'BAT/USD'],

    'kraken': ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'LTC/EUR', 'BCH/USD',
               'BCH/EUR', 'BCH/BTC', 'XRP/USD', 'XRP/EUR', 'XRP/BTC', 'EOS/BTC', 'EOS/ETH', 'DASH/BTC', 'DASH/EUR',
               'XMR/EUR', 'REP/ETH', 'REP/EUR', 'REP/BTC', 'XMR/USD', 'ETC/USD', 'ETC/EUR', 'DASH/USD', 'ETC/BTC',
               'ZEC/BTC'
        , 'BTC/CAD', 'ZEC/USD', 'ZEC/EUR', 'ETH/CAD', 'XLM/BTC', 'XDG/BTC', 'MLN/BTC', 'ICN/ETH', 'ICN/BTC', 'GNO/BTC',
               'GNO/ETH'],

    'binance': ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC', 'EOS/BTC',
                'EOS/ETH', 'BCH/ETH', 'IOTA/BTC', 'IOTA/ETH', 'NEO/USDT', 'NEO/BTC', 'NEO/ETH', 'DASH/BTC', 'OMG/BTC',
                'OMG/ETH', 'BTG/BTC', 'BTG/ETH', 'QTUM/BTC', 'TRX/BTC', 'ZRX/BTC', 'BAT/BTC']
    ,
    'bitstamp': ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'LTC/EUR', 'BCH/USD',
                 'BCH/EUR', 'BCH/BTC', 'XRP/USD', 'XRP/EUR', 'XRP/BTC']
    ,
    'btcturk': ['BTC/TRY', 'ETH/TRY', 'XRP/TRY']
    ,
    'huobipro': ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC', 'EOS/BTC',
                 'EOS/ETH', 'NEO/USDT', 'NEO/BTC', 'DASH/BTC', 'DASH/USDT', 'ELF/USDT', 'OMG/BTC', 'OMG/ETH', 'BTG/BTC',
                 'QTUM/BTC', 'TRX/BTC', 'ZRX/BTC', 'BAT/BTC', 'HT/USDT', 'HT/BTC', 'IOST/USDT', 'ELA/BTC', 'MDS/BTC',
                 'ELA/ETH', 'IOST/BTC']
    ,
    'hitbtc': ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC', 'EOS/BTC',
               'EOS/ETH', 'BCH/ETH', 'NEO/USDT', 'NEO/BTC', 'NEO/ETH', 'DASH/BTC', 'OMG/BTC', 'OMG/ETH', 'BTG/BTC',
               'BTG/ETH', 'QTUM/BTC', 'ETP/BTC', 'TRX/BTC', 'ZRX/BTC']
    ,
    'bitbay': ['BTC/PLN', 'LSK/PLN', 'ETH/PLN', 'LTC/PLN', 'GAME/PLN', 'BCH/PLN', 'BTG/PLN', 'DASH/PLN', 'LSK/EUR',
               'LSK/BTC']
    ,
    'bl3p': ['BTC/EUR', 'LTC/EUR']
    ,
    'btcmarkets': ['BTC/AUD', 'LTC/AUD', 'ETH/AUD', 'BCH/AUD', 'ETC/AUD', 'XRP/AUD', 'LTC/BTC', 'ETH/BTC', 'ETC/BTC',
                   'XRP/BTC', 'BCH/BTC']
    ,
    'coinfloor': ['BTC/USD', 'BTC/EUR', 'BTC/GBP', 'BCH/GBP']
    ,
    'gemini': ['BTC/USD', 'ETH/USD', 'ETH/BTC']
    ,
    'tidex': ['WAVES/BTC', 'ETH/BTC', 'IDH/ETH', 'TIE/BTC', 'BCH/BTC', 'BTC/USDT', 'BAR/ETH', 'KOLION/WAVES', 'AGI/BTC',
              'ETH/USDT', 'WAVES/ETH', 'BCH/WAVES']
    ,
    'cex': ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'ETH/GBP', 'BTC/USD', 'BTC/EUR', 'BTC/GBP', 'BCH/USD', 'BCH/EUR',
            'BCH/BTC', 'XRP/USD', 'XRP/BTC', 'XRP/EUR', 'ZEC/USD', 'ZEC/EUR', 'ZEC/BTC', 'BTC/RUB', 'XLM/BTC',
            'XLM/EUR', 'XLM/USD', 'DASH/BTC', 'DASH/EUR', 'DASH/USD', 'BTG/BTC', 'BTG/EUR', 'BTG/USD']
    ,
    'koineks': ['ETH', 'BTC', 'LTC', 'XRP', 'XLM', 'DOGE', 'DASH', 'XEM']

}

exchange_list = ['gdax', 'bitfinex', 'kraken', 'binance', 'bitstamp', 'btcturk', 'huobipro', 'hitbtc', 'bl3p',
                 'btcmarkets', 'coinfloor', 'gemini', 'tidex', 'bitbay', 'cex']

ticker_exchange_list = ['bitstamp', 'btcturk', 'bitbay', 'bl3p', 'btcmarkets', 'coinfloor', 'gemini', 'tidex', 'cex',
                        'koineks']

gdax_currency = ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'BTC/GBP', 'LTC/USD', 'LTC/EUR', 'LTC/BTC',
                 'BCH/USD', 'BCH/EUR', 'BCH/BTC']

bitfinex_currency = ['ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'BCH/USD', 'BCH/BTC', 'XRP/USD',
                     'XRP/BTC', 'EOS/USD', 'EOS/BTC', 'EOS/ETH', 'BCH/ETH', 'IOTA/EUR', 'IOTA/USD', 'IOTA/BTC',
                     'IOTA/ETH', 'NEO/USD', 'NEO/BTC', 'NEO/ETH', 'DASH/BTC', 'ELF/USD', 'OMG/USD', 'BTG/USD',
                     'SAN/USD', 'QTUM/USD', 'ETP/USD', 'TRX/USD', 'ZRX/USD', 'BAT/USD']

kraken_currency = ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'LTC/EUR', 'BCH/USD',
                   'BCH/EUR', 'BCH/BTC', 'XRP/USD', 'XRP/EUR', 'XRP/BTC', 'EOS/BTC', 'EOS/ETH', 'DASH/BTC', 'DASH/EUR',
                   'XMR/EUR', 'REP/ETH', 'REP/EUR', 'REP/BTC', 'XMR/USD', 'ETC/USD', 'ETC/EUR', 'DASH/USD', 'ETC/BTC',
                   'ZEC/BTC'
    , 'BTC/CAD', 'ZEC/USD', 'ZEC/EUR', 'ETH/CAD', 'XLM/BTC', 'XDG/BTC', 'MLN/BTC', 'ICN/ETH', 'ICN/BTC', 'GNO/BTC',
                   'GNO/ETH']

binance_currency = ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC',
                    'EOS/BTC', 'EOS/ETH', 'BCH/ETH', 'IOTA/BTC', 'IOTA/ETH', 'NEO/USDT', 'NEO/BTC', 'NEO/ETH',
                    'DASH/BTC', 'OMG/BTC', 'OMG/ETH', 'BTG/BTC', 'BTG/ETH', 'QTUM/BTC', 'TRX/BTC', 'ZRX/BTC', 'BAT/BTC']

bitstamp_currency = ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'BTC/USD', 'BTC/EUR', 'LTC/USD', 'LTC/BTC', 'LTC/EUR', 'BCH/USD',
                     'BCH/EUR', 'BCH/BTC', 'XRP/USD', 'XRP/EUR', 'XRP/BTC']

btcturk_currency = ['BTC/TRY', 'ETH/TRY', 'XRP/TRY']

huobipro_currency = ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC',
                     'EOS/BTC', 'EOS/ETH', 'NEO/USDT', 'NEO/BTC', 'DASH/BTC', 'DASH/USDT', 'ELF/USDT', 'OMG/BTC',
                     'OMG/ETH', 'BTG/BTC', 'QTUM/BTC', 'TRX/BTC', 'ZRX/BTC', 'BAT/BTC', 'HT/USDT', 'HT/BTC',
                     'IOST/USDT', 'ELA/BTC', 'MDS/BTC', 'ELA/ETH', 'IOST/BTC']

hitbtc_currency = ['ETH/USDT', 'ETH/BTC', 'BTC/USDT', 'LTC/USDT', 'LTC/BTC', 'BCH/USDT', 'BCH/BTC', 'XRP/BTC',
                   'EOS/BTC', 'EOS/ETH', 'BCH/ETH', 'NEO/USDT', 'NEO/BTC', 'NEO/ETH', 'DASH/BTC', 'OMG/BTC', 'OMG/ETH',
                   'BTG/BTC', 'BTG/ETH', 'QTUM/BTC', 'ETP/BTC', 'TRX/BTC', 'ZRX/BTC']

bitbay_currency = ['BTC/PLN', 'LSK/PLN', 'ETH/PLN', 'LTC/PLN', 'GAME/PLN', 'BCH/PLN', 'BTG/PLN', 'DASH/PLN', 'LSK/EUR',
                   'LSK/BTC']

bl3p_currency = ['BTC/EUR', 'LTC/EUR']

btcmarkets_currency = ['BTC/AUD', 'LTC/AUD', 'ETH/AUD', 'BCH/AUD', 'ETC/AUD', 'XRP/AUD', 'LTC/BTC', 'ETH/BTC',
                       'ETC/BTC', 'XRP/BTC', 'BCH/BTC']

coinfloor_currency = ['BTC/USD', 'BTC/EUR', 'BTC/GBP', 'BCH/GBP']

gemini_currency = ['BTC/USD', 'ETH/USD', 'ETH/BTC']

tidex_currency = ['WAVES/BTC', 'ETH/BTC', 'IDH/ETH', 'TIE/BTC', 'BCH/BTC', 'BTC/USDT', 'BAR/ETH', 'KOLION/WAVES',
                  'AGI/BTC', 'ETH/USDT', 'WAVES/ETH', 'BCH/WAVES']

cex_currency = ['ETH/EUR', 'ETH/USD', 'ETH/BTC', 'ETH/GBP', 'BTC/USD', 'BTC/EUR', 'BTC/GBP', 'BCH/USD', 'BCH/EUR',
                'BCH/BTC', 'XRP/USD', 'XRP/BTC', 'XRP/EUR', 'ZEC/USD', 'ZEC/EUR', 'ZEC/BTC', 'BTC/RUB', 'XLM/BTC',
                'XLM/EUR', 'XLM/USD', 'DASH/BTC', 'DASH/EUR', 'DASH/USD', 'BTG/BTC', 'BTG/EUR', 'BTG/USD']

koineks_currency = ['ETH', 'BTC', 'LTC', 'XRP', 'XLM', 'DOGE', 'DASH', 'XEM']

koineks_pair = {'ETH': 'ETH/TRY', 'BTC': 'BTC/TRY', 'LTC': 'LTC/TRY', 'XRP': 'XRP/TRY',
                'XLM': 'XLM/TRY', 'DOGE': 'DOGE/TRY', 'DASH': 'DASH/TRY', 'XEM': 'XEM/TRY'
                }

# DEFINE DATABASE CONNECTIONS

gdax_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/gdax')
bitfinex_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/bitfinex')
huobipro_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/huobipro')
kraken_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/kraken')
binance_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/binance')
bitstamp_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/bitstamp')
btcturk_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/btcturk')
hitbtc_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/hitbtc')
bitbay_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/bitbay')
bl3p_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/bl3p')
btcmarkets_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/btcmarkets')
coinfloor_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/coinfloor')
gemini_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/gemini')
tidex_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/tidex')
cex_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/cex')
koineks_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/koineks')

# DEFINE DATABASE CONNECTION FOR TECHNICAL INDICATORS
indicator_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/indicators')
historical_db = dataset.connect('mysql://remote_user:y6B-eyS-aCx-BEA@139.59.147.221/historical')

gdax = ccxt.gdax({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "gdax",
    'database': gdax_db
})

bitfinex = ccxt.bitfinex({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "bitfinex",
    'database': bitfinex_db
})

huobipro = ccxt.huobipro({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "huobipro",
    'database': huobipro_db
})

kraken = ccxt.kraken({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "kraken",
    'database': kraken_db
})

binance = ccxt.binance({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "binance"
    , 'database': binance_db
})

bitstamp = ccxt.bitstamp({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "bitstamp",
    'database': bitstamp_db
})

btcturk = ccxt.btcturk({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "btcturk",
    'database': btcturk_db
})

hitbtc = ccxt.hitbtc2({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "hitbtc"
    , 'database': hitbtc_db
})

bitbay = ccxt.bitbay({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "bitbay",
    'database': bitbay_db
})

bl3p = ccxt.bl3p({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "bl3p"
    , 'database': bl3p_db
})

btcmarkets = ccxt.btcmarkets({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "btcmarkets"
    , 'database': btcmarkets_db
})

coinfloor = ccxt.coinfloor({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "coinfloor",
    'database': coinfloor_db
})

gemini = ccxt.gemini({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "gemini",
    'database': gemini_db
})

tidex = ccxt.tidex({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "tidex",
    'database': tidex_db
})

cex = ccxt.cex({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    'exchangeName': "cex",
    'database': cex_db
})


def koineks_ticker(currency):
    # To use this function, instead of calling a currency pair, just use BTC, ETH, XLM, LTC, DASH,XRP,DOGE

    # Because of pair api response is different than other api calls, there is another dict called koineks_pair to normalize it.

    try:
        exchange = {'database': koineks_db, 'name': 'koineks'}
        data = requests.get('https://koineks.com/ticker')
        high = data.json()[currency]['high']
        low = data.json()[currency]['low']
        closing = float(data.json()[currency]['current'])
        volume = data.json()[currency]['volume']
        timestamp = data.json()[currency]['timestamp']
        ask = data.json()[currency]['ask']
        bid = data.json()[currency]['bid']

        # Check if there is empty values. Sometimes, some apis doesnt have values
        # and this causes problems in database records.

        if not high:
            high = 0
        if not low:
            low = 0
        if not volume:
            volume = 0
        if not bid:
            bid = 0
        if not ask:
            ask = 0

        trading_pairs = {
            "trading_pair_id": 'koineks' + '_' + str(koineks_pair[currency]).replace("/", "_").lower(),
            "trading_pair": koineks_pair[currency],
            "price": closing,
            "price_delta_1h": None,
            "price_delta_24h": None,
            "price_updated_at": timestamp
        }
        sleep(0.035)

        print (exchange.database)

        database_write(exchange, currency, timestamp, 0, high, closing, low, volume, ask, bid)

    except Exception as error:
        print('got an error in koineks ticker fetching' + str(error))
    return (trading_pairs)


def koineks_update(pairs):
    firebase_pairs = []

    firebase_payload = {
        "id": 'koineks',
        "name": 'KOINEKS',
        "trading_pairs": firebase_pairs
    }
    # Cycle through pairs to push prices to firebase.
    try:
        for x in pairs:
            data = koineks_ticker(x)
            print("Fetching data from Koineks for " + str(x))
            firebase_pairs.append(data)
        firebase_prices_push(firebase_payload)

    except Exception as error:
        print("error in koineks ticker fetching. Error: " + str(error))


def candle24h(exchange, currency):
    try:
        start_date = datetime.datetime.utcnow() + datetime.timedelta(-1)
        # following line is in milliseconds
        # kraken has a different candle response. Because of this there should be an additional code to check
        # what is the timestamp order is.
        from_timestamp = exchange.parse8601(str(start_date))
        candles = exchange.fetch_ohlcv(currency, '5m', from_timestamp, 288)

        # check the candle order by looking at the timestamps of the list.
        if candles[0][0] < candles[-1][0]:
            opening = candles[-1][1]
            high = candles[-1][2]
            low = candles[-1][3]
            closing = candles[-1][4]
            volume = candles[-1][5]

            price_1h = candles[-11][4]
            price_24h = candles[0][4]
            delta1h = (closing - price_1h) / closing * 100
            delta24h = (closing - price_24h) / closing * 100
            timestamp = candles[-1][0]


        else:
            opening = candles[0][1]
            high = candles[0][2]
            low = candles[0][3]
            closing = candles[0][4]
            volume = candles[0][5]

            price_1h = candles[11][4]
            price_24h = candles[-1][4]
            delta1h = (closing - price_1h) / closing * 100
            delta24h = (closing - price_24h) / closing * 100
            timestamp = candles[0][0]

        trading_pairs = {
            "trading_pair_id": id_convert(exchange, currency),
            "trading_pair": currency,
            "price": float(closing),
            "price_delta_1h": float(delta1h),
            "price_delta_24h": float(delta24h),
            "price_updated_at": timestamp
        }

        # Write all that shit into database

        database_write(exchange, currency, timestamp, opening, high, closing, low, volume, 0, 0)

        sleep(exchange.rateLimit / 1000)

    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:

        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')

        sleep(exchange.rateLimit / 1000)

    return trading_pairs


def ticker(exchange, currency):
    try:
        ticker = exchange.fetch_ticker(currency)

        closing = ticker['last']
        timestamp = ticker['timestamp']
        open = ticker['open']
        high = ticker['high']
        low = ticker['low']
        volume = ticker['baseVolume']
        bid = ticker['bid']
        ask = ticker['ask']

        # Check if there is empty values. Sometimes, some apis doesnt have values
        # and this causes problems in database records.

        if not open:
            open = 0
        if not high:
            high = 0
        if not low:
            low = 0
        if not volume:
            volume = 0
        if not bid:
            bid = 0
        if not ask:
            ask = 0

        delta = ticker_delta(exchange, currency)
        # check if delta is giving None data.
        if not delta:

            trading_pairs = {
                "trading_pair_id": id_convert(exchange, currency),
                "trading_pair": currency,
                "price": float(closing),
                "price_delta_1h": None,
                "price_delta_24h": None,
                "price_updated_at": timestamp
            }
        else:

            trading_pairs = {
                "trading_pair_id": id_convert(exchange, currency),
                "trading_pair": currency,
                "price": float(closing),
                "price_delta_1h": delta[0],
                "price_delta_24h": delta[1],
                "price_updated_at": timestamp
            }

        database_write(exchange, currency, timestamp, open, high, closing, low, volume, bid, ask)

        sleep(exchange.rateLimit / 1000)
    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        sleep(exchange.rateLimit / 1000)
    return trading_pairs


def candle_update(exchange, pairs):
    firebase_pairs = []

    firebase_payload = {
        "id": str(exchange.exchangeName),
        "name": str(exchange.exchangeName).upper(),
        "trading_pairs": firebase_pairs
    }

    try:
        for x in pairs:
            data = candle24h(exchange, x)
            print("Fetching data from " + str(exchange) + " for " + str(x))
            firebase_pairs.append(data)
        firebase_prices_push(firebase_payload)

    except Exception as error:
        print("error " + str(exchange) + " in candle fetching. Error: " + str(error))


def ticker_update(exchange, pairs):
    firebase_pairs = []

    firebase_payload = {
        "id": str(exchange.exchangeName),
        "name": str(exchange.exchangeName).upper(),
        "trading_pairs": firebase_pairs
    }

    try:
        for x in pairs:
            data = ticker(exchange, x)
            print("writing data for " + str(x))
            firebase_pairs.append(data)
        firebase_prices_push(firebase_payload)

    except Exception as error:
        print("error " + str(exchange) + " in ticker fetching. Error: " + str(error))


def firebase_exchanges():
    payload_2 = []

    for x in xrange(13):
        payload_1 = {
            "id": exchange_list[x],
            "name": exchange_list[x],
            "trading_pairs": exchange_dict[exchange_list[x]],
        }
        payload_2.append(payload_1)
    payload_out = json.dumps(payload_2)
    headers = {
        'content-type': "application/json"
    }

    url = "https://us-central1-krypto2017-1.cloudfunctions.net/exchanges"
    response = requests.request("POST", url, data=payload_out, headers=headers)
    print(response.text)
    print(payload_2)
    print("payload generated for: " + str(x))


def id_convert(exchange, pair):
    id = str(exchange.exchangeName) + '_' + str(pair).replace("/", "_").lower()
    return id


def firebase_prices_push(data):
    try:
        payload_out = json.dumps(data)
        headers = {
            'content-type': "application/json"
        }

        url = "https://us-central1-krypto2017-1.cloudfunctions.net/prices"
        response = requests.request("POST", url, data=payload_out, headers=headers)
        print(response.text)
        print("payload generated")
    except Exception as error:
        print ("Error occured while pushing to Firebase " + str(error))


def ecb_fetch():
    try:
        # Fetch XML data from European Central Exchange for EUR Fiat currencies.

        file = urllib2.urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        data = file.read()
        file.close()
        result = xmltodict.parse(data)

        # Filter the data of the dictionary get rid of un useful parts.

        filtered_data = result['gesmes:Envelope']['Cube']['Cube']

        timestamp_date = filtered_data['@time']

        firebase_pairs = []

        firebase_payload = {
            "id": str("ecb"),
            "name": str("ECB"),
            "trading_pairs": firebase_pairs
        }
        for x in xrange(32):
            currency = filtered_data['Cube'][x]['@currency']
            closing = float(filtered_data['Cube'][x]['@rate'])
            trading_pairs = {
                "trading_pair_id": 'ecb' + '_' + 'eur_' + str(currency).lower(),
                "trading_pair": 'EUR/' + str(currency),
                "price": closing,
                "price_delta_1h": None,
                "price_delta_24h": None,
                "price_updated_at": int(round(time.time() * 1000))  # ms timestamp
            }
            firebase_pairs.append(trading_pairs)
        firebase_prices_push(firebase_payload)
        print("Fetched and pushed European Central Bank Pairs into Firebase")
    except Exception as error:
        print ("error in European Central Bank Data Fetching" + str(error))

def database_write(exchange, currency, timestamp, opening, high, close, low, volume, bid, ask):
    exchange.database.begin()

    exchange.database[currency].insert(dict(time_ms=long(timestamp), opening=float(opening), high=float(high),
                                            close=float(close), low=float(low), volume=float(volume), bid=float(bid),
                                            ask=float(ask)))

    exchange.database.commit()


def ticker_delta(exchange, currency):
    try:
        table = exchange.database[currency]

        ticker_length = len(table)

        # Check if there is enough candles in database for delta calculation.

        if ticker_length > 10:

            time_between_tickers_min = (float(table.find_one(id='10')['time_ms']) - float(
                table.find_one(id='1')['time_ms'])) / 10 / 60000

            delta1h_ticker_count = int(time_between_tickers_min * 60)

            delta24h_ticker_count = int(time_between_tickers_min * 60 * 24)
        else:

            delta1h_ticker_count = 0

            delta24h_ticker_count = 0

        print ("delta1h ticker count " + str(delta1h_ticker_count))
        print ("delta24h ticker count " + str(delta1h_ticker_count))

        last_ticker = table.find_one(id=str(ticker_length))['close']

        if 0 < delta24h_ticker_count < ticker_length:

            delta24h_ticker = int(table.find_one(id=str(ticker_length - delta24h_ticker_count))['close'])

            delta24h = ((last_ticker - delta24h_ticker) / last_ticker) * 100

        else:

            delta24h = None

        if 0 < delta1h_ticker_count < ticker_length:

            delta1h_ticker = int(table.find_one(id=str(ticker_length - delta1h_ticker_count))['close'])

            delta1h = ((last_ticker - delta1h_ticker) / last_ticker) * 100

        else:

            delta1h = None
        print (str(currency) + " delta 1h: " + str(delta1h))
        print (str(currency) + " delta 24h: " + str(delta24h))

    except Exception as error:
        print (error)
        delta24h = None
        delta1h = None
    return (delta1h, delta24h)

def update_all():
    while (True):
        try:
            # bitstamp,btcturk,bitbay,bl3p,btcmarkets,coinfloor,gemini,tidex candles doesnt work.
            ticker_update(gdax, gdax_currency)
            ticker_update(kraken, kraken_currency)
            ticker_update(bitfinex, bitfinex_currency)
            ticker_update(binance, binance_currency)
            ticker_update(huobipro, huobipro_currency)
            ticker_update(hitbtc, hitbtc_currency)
            # candle_update(cex, cex_currency) This guy is not responding to candles.
            # ticker updates
            ticker_update(bitstamp, bitstamp_currency)
            ticker_update(btcturk, btcturk_currency)
            ticker_update(bitbay, bitbay_currency)
            ticker_update(bl3p, bl3p_currency)
            ticker_update(btcmarkets, btcmarkets_currency)
            ticker_update(coinfloor, coinfloor_currency)
            ticker_update(gemini, gemini_currency)
            ticker_update(tidex, tidex_currency)
            ticker_update(cex, cex_currency)
            koineks_update(koineks_currency)
            ecb_fetch()
        except:
            print("error in update all function")


update_all()

