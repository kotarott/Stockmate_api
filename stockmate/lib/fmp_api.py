from django.conf import settings
import requests

# API_KEY = settings.FMP_API_KEY
# FMP_V3 = settings.FMP_V3

# test
API_KEY = '6d5d08c107b889767b1b8cb5a3febfe4'
FMP_V3 = 'https://financialmodelingprep.com/api/v3/'

def request_url(url, query, timeout=2.0):
    r = requests.get(url, params=query, timeout=timeout)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def search_symbol(keyword, limit=10, exchange=None):
    url = FMP_V3 + 'search'
    query = {
        'query': keyword,
        'limit': limit,
        'apikey': API_KEY
    }
    if exchange:
        query['exchange'] = exchange
    return request_url(url, query)

def get_profile(symbol):
    url = FMP_V3 + 'profile/' + symbol
    query = {
        'apikey': API_KEY
    }
    return request_url(url, query)

def get_historical_price(symbol, serietype='line', to_date=None, from_date=None, timeseries=None):
    url = FMP_V3 + 'historical-price-full/' + symbol
    query = {
        'serietype': serietype,
        'apikey': API_KEY
    }
    if to_date:
        query['to'] = to_date
    if from_date:
        query['from'] = from_date
    if timeseries:
        query['timeseries'] = timeseries
    return request_url(url, query, 5.0)

def get_income_statement(symbol, limit=120, period=None):
    url = FMP_V3 + 'income-statement/' + symbol
    query = {
        'limit': limit,
        'apikey': API_KEY
    }
    if period:
        query['period'] = period
    return request_url(url, query, 5.0)

def get_ndx_list():
    url = FMP_V3 + 'nasdaq_constituent/'
    query = {
        'apikey': API_KEY
    }
    return request_url(url, query, 5.0)

def get_key_metric(symbol, limit=1, period=None):
    url = FMP_V3 + 'key-metrics-ttm/' + symbol
    query = {
        'limit': limit,
        'apikey': API_KEY
    }
    if period:
        query['period'] = period
    return request_url(url, query, 2.0)

def get_financial_growth(symbol, limit=1, period=None):
    url = FMP_V3 + 'financial-growth/' + symbol
    query = {
        'limit': limit,
        'apikey': API_KEY
    }
    if period:
        query['period'] = period
    return request_url(url, query, 2.0)

if __name__ == ('__main__'):
    # search_symbol("SONY")
    # print(get_profile('AAPL'))
    pass