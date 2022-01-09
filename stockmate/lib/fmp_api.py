from django.conf import settings
import requests

API_KEY = settings.FMP_API_KEY
FMP_V3 = settings.FMP_V3

def search_symbol(keyword, limit=10, exchange=None):
    url = FMP_V3 + 'search'
    query = {
        'query': keyword,
        'limit': limit,
        'apikey': API_KEY
    }
    if exchange:
        query['exchange'] = exchange
    r = requests.get(url, params=query, timeout=2.0)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

if __name__ == ('__main__'):
    search_symbol("SONY")
