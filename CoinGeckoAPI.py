import requests
import pandas as pd

class CoinGeckoAPI:

    @classmethod
    def initialize(cls):
        cls.url = 'https://api.coingecko.com/api/v3/'
    
    @classmethod
    def __api(cls, end_point):
        return requests.get(cls.url + end_point).json()

    @classmethod
    def __api_params(cls, end_point, params):
        return requests.request('GET', cls.url + end_point, params=params).json()

    @classmethod
    def ping(cls):
        return cls.__api('ping')
    
    @classmethod
    def getCoinList(cls):
        return cls.__api('coins/list')


    '''
    [{'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'image': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579', 'current_price': 66184, 'market_cap': 1239021452561, 'market_cap_rank': 1, 'fully_diluted_valuation': 1378628533613, 'total_volume': 26876258787, 'high_24h': 66081, 'low_24h': 63705, 'price_change_24h': 1277.87, 'price_change_percentage_24h': 1.96879, 'market_cap_change_24h': 18721730710, 'market_cap_change_percentage_24h': 1.53419, 'circulating_supply': 18873431.0, 'total_supply': 21000000.0, 'max_supply': 21000000.0, 'ath': 69045, 'ath_change_percentage': -4.1431, 'ath_date': '2021-11-10T14:24:11.849Z', 'atl': 67.81, 'atl_change_percentage': 97503.81785, 'atl_date': '2013-07-06T00:00:00.000Z', 'roi': None, 'last_updated': '2021-11-15T00:18:54.919Z'}]
    '''
    @classmethod
    def getCoinData(cls, coin_id):
        return cls.__api_params('/coins/markets', {"ids" : coin_id,"vs_currency" : "usd"})



    @classmethod
    def test(cls):
        return cls.__api_params('/coins/markets', {"ids" : "bitcoin","vs_currency" : "usd"})

if __name__ == '__main__':
    CoinGeckoAPI.initialize()
    print(CoinGeckoAPI.test())
    #print(CoinGeckoAPI.ping())