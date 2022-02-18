import ccxt
import time
import datetime
import threading
import pandas as pd
from datetime import datetime




'''
you can theoretically get out roughly 20 orders per second per subaccount if they are evenly spaced out without experiencing higher latency.

'''
class FTXApi:
    @classmethod
    def initialize(cls):
        cls.secret_key = ''
        cls.api_key = ''
        cls.__read_keys()
        cls.ftx = ccxt.ftx({
            'apiKey': cls.api_key,
            'secret': cls.secret_key,
            'headers':{'FTX-SUBACCOUNT': 'Bot'},
        })
    
    @classmethod
    def __read_keys(cls):
        file = open('./ignore/api_key.txt', 'r')  # 読み込みモードでオープン
        cls.secret_key = file.readline().split(':')[1]
        cls.secret_key = cls.secret_key[:len(cls.secret_key) - 1]
        cls.api_key = file.readline().split(':')[1]
        cls.api_key = cls.api_key[:len(cls.api_key) - 1]
        file.close()


    ''''
    info': {'name': 'XTZHALF/USD', 'enabled': True, 'postOnly': False, 'priceIncrement': '0.5', 'sizeIncrement': '0.00001', 'minProvideSize': '0.00001', 'last': '11262.0', 'bid': '11216.5', 'ask': '11230.5', 'price': '11230.5', 'type': 'spot', 'baseCurrency': 'XTZHALF', 'quoteCurrency': 'USD', 'underlying': None, 'restricted': False, 'highLeverageFeeExempt': True, 'change1h': '-0.0018664178109585388', 'change24h': '-0.00026705835224996664', 'changeBod': '-0.0018664178109585388', 'quoteVolume24h': '0.56247', 'volumeUsd24h': '0.56247'}}, 
    {'id': 'XTZHEDGE/USD', 'symbol': 'XTZHEDGE/USD', 'base': 'XTZHEDGE', 'quote': 'USD', 'baseId': 'XTZHEDGE', 'quoteId': 'USD', 'type': 'spot', 'future': False, 'spot': True, 'active': True, 'precision': {'amount': 0.001, 'price': 0.005}, 'limits': {'amount': {'min': 0.001, 'max': None}, 'price': {'min': 0.005, 'max': None}, 'cost': {'min': None, 'max': None}, 'leverage': {'max': 20}}, 'info': {'name': 'XTZHEDGE/USD', 'enabled': True, 'postOnly': False, 'priceIncrement': '0.005', 'sizeIncrement': '0.001', 'minProvideSize': '0.001', 'last': '58.42', 'bid': '58.395', 'ask': '58.52', 'price': '58.42', 'type': 'spot', 'baseCurrency': 'XTZHEDGE', 'quoteCurrency': 'USD', 'underlying': None, 'restricted': False, 'highLeverageFeeExempt': True, 'change1h': '0.0', 'change24h': '0.0038663115387919922', 'changeBod': '0.0', 'quoteVolume24h': '0.40773', 'volumeUsd24h': '0.40773'}}, 
    {'id': 'ZECBEAR/USD', 'symbol': 'ZECBEAR/USD', 'base': 'ZECBEAR', 'quote': 'USD', 'baseId': 'ZECBEAR', 'quoteId': 'USD', 'type': 'spot', 'future': False, 'spot': True, 'active': True, 'precision': {'amount': 1.0, 'price': 0.0001}, 'limits': {'amount': {'min': 1.0, 'max': None}, 'price': {'min': 0.0001, 'max': None}, 'cost': {'min': None, 'max': None}, 'leverage': {'max': 20}}, 'info': {'name': 'ZECBEAR/USD', 'enabled': True, 'postOnly': False, 'priceIncrement': '0.0001', 'sizeIncrement': '1.0', 'minProvideSize': '1.0', 'last': '0.2678', 'bid': '0.258', 'ask': '0.2614', 'price': '0.2614', 'type': 'spot', 'baseCurrency': 'ZECBEAR', 'quoteCurrency': 'USD', 'underlying': None, 'restricted': False, 'highLeverageFeeExempt': True, 'change1h': '-0.01544256120527307', 'change24h': '-0.10571330824495381', 'changeBod': '-0.01321253303133258', 'quoteVolume24h': '1281.8555', 'volumeUsd24h': '1281.8555'}}, 
    {'id': 'ZECBULL/USD', 'symbol': 'ZECBULL/USD', 'base': 'ZECBULL', 'quote': 'USD', 'baseId': 'ZECBULL', 'quoteId': 'USD', 'type': 'spot', 'future': False, 'spot': True, 'active': True, 'precision': {'amount': 0.1, 'price': 0.00025}, 'limits': {'amount': {'min': 0.1, 'max': None}, 'price': {'min': 0.00025, 'max': None}, 'cost': {'min': None, 'max': None}, 'leverage': {'max': 20}}, 'info': {'name': 'ZECBULL/USD', 'enabled': True, 'postOnly': False, 'priceIncrement': '0.00025', 'sizeIncrement': '0.1', 'minProvideSize': '0.1', 'last': '0.7335', 'bid': '0.725', 'ask': '0.73325', 'price': '0.73325', 'type': 'spot', 'baseCurrency': 'ZECBULL', 'quoteCurrency': 'USD', 'underlying': None, 'restricted': False, 'highLeverageFeeExempt': True, 'change1h': '0.01911049339819319', 'change24h': '0.12246460007654038', 'changeBod': '0.00963855421686747', 'quoteVolume24h': '22862.55735', 'volumeUsd24h': '22862.55735'}}]
    '''
    @classmethod
    def fetch_market(cls):
        return cls.ftx.fetch_markets()


    '''
    Index(['name', 'underlying', 'description', 'type', 'expiry', 'perpetual',
       'expired', 'enabled', 'postOnly', 'priceIncrement', 'sizeIncrement',
       'last', 'bid', 'ask', 'index', 'mark', 'imfFactor', 'lowerBound',
       'upperBound', 'underlyingDescription', 'expiryDescription', 'moveStart',
       'marginPrice', 'positionLimitWeight', 'group', 'change1h', 'change24h',
       'changeBod', 'volumeUsd24h', 'volume', 'openInterest',
       'openInterestUsd'],
      dtype='object')

  name underlying                        description       type  ...   volumeUsd24h      volume  openInterest  openInterestUsd
0    1INCH-PERP      1INCH      1INCH Token Perpetual Futures  perpetual  ...   35650146.967   9903438.0     8511947.0    30248054.8592
1    1INCH-1231      1INCH  1INCH Token December 2021 Futures     future  ...    378150.1963    108447.0      499588.0     1688157.8108
2     AAPL-1231       AAPL        Apple December 2021 Futures     future  ...    200801.1765     1233.08       1053.75      175143.7875
3     AAVE-PERP       AAVE             Aave Perpetual Futures  perpetual  ...  26027528.5512    101584.1      61071.55    16099071.2955
4     AAVE-1231       AAVE         Aave December 2021 Futures     future  ...    168483.5163      651.98       4898.73     1308695.7195

    '''
    @classmethod
    def get_future(cls):
        df= pd.DataFrame(cls.ftx.fetch('https://ftx.com/api/futures'))
        df_list = pd.DataFrame(df['result'].to_list())
        return df_list[(df_list['enabled']==True)]

    '''
    {'success': True, 'result': {'username': 'securities.alunfes@gmail.com/Bot', 'collateral': '0.0', 'freeCollateral': '0.0', 'totalAccountValue': '0.0', 'totalPositionSize': '0.0', 'initialMarginRequirement': '0.1', 'maintenanceMarginRequirement': '0.03', 'marginFraction': None, 'openMarginFraction': None, 'liquidating': False, 'backstopProvider': False, 'positions': [], 'takerFee': '0.00044', 'makerFee': '-0.00001', 'leverage': '10.0', 'positionLimit': None, 'positionLimitUsed': None, 'useFttCollateral': True, 'chargeInterestOnNegativeUsd': False, 'spotMarginEnabled': False, 'spotLendingEnabled': False}}
    '''
    @classmethod
    def fetch_account(cls):
        return cls.ftx.private_get_account()

    '''
    max=1500
    sinceは通常のunixtime * 1000
    [[1636333920000, 65368.0, 65384.0, 65306.0, 65349.0, 66.36970000000001, 472], [1636333980000, 65350.0, 65373.0, 65255.0, 65257.0, 83.30500000000006, 612], [1636334040000, 65257.0, 65311.0, 65257.0, 65288.0, 84.1160000000001, 608], [1636334100000, 65287.0, 65453.0, 65287.0, 65304.0, 140.41200000000018, 1041], [1636334160000, 65303.0, 65354.0, 65295.0, 65310.0, 69.03869999999996, 466], [1636334220000, 65314.0, 65360.0, 65272.0, 65319.0, 77.79839999999997, 691], [1636334280000, 65319.0, 65333.0, 65217.0, 65286.0, 150.19779999999986, 917], [1636334340000, 65280.0, 65286.0, 65235.0, 65241.0, 25.117399999999996, 192]]
    '''
    @classmethod
    def get_ohlc(cls, symbol, timeframe, since):
        return cls.ftx.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since)
        

    @classmethod
    def measure_server_responding_time(cls):
        start_time = time.perf_counter()
        cls.ftx.fetch_status()
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)


    @classmethod
    def test(cls):
        start_time = time.perf_counter()
        print(cls.ftx.fetch_status())
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(elapsed_time)



if __name__ == '__main__':
    #for historical data download
    FTXApi.initialize()
    #since = int(time.time() / 2.0)*1000
    #print(FTXApi.get_ohlc('BTC-PERP', '1m', since))

    FTXApi.test()

    #futures = FTXApi.get_future()
    #df=futures[(futures['type']=='perpetual')].reset_index()
    #df.to_csv('./data.csv')
    #print(futures[(futures['enabled']=='true') & (futures['type']=='perpetual')])
    #df = pd.DataFrame(FTXApi.fetch_market())
    #df_list = pd.DataFrame(df['info'].to_list())
    #print(df_list[(df_list['enabled']==True) & (df_list['future']==True)])
    #FTXApi.test()
    