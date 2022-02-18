from fileinput import filename
import pandas as pd
import time
import os
import sys
from datetime import datetime
from FTXApi import FTXApi




class MarketData:
    '''
    既存のファイルに現時点までのデータを追記する。
    '''
    @classmethod
    def addOhlcv(cls, minutes, perp_name):
        ori_df = cls.readOhlcvFile(perp_name+'-'+str(minutes)+'m.csv')
        print('oroginal df:')
        print(ori_df)
        since = int(ori_df['ts'].iloc[-1])
        FTXApi.initialize()
        all_df = pd.DataFrame()
        print('MarketData.addOhlcv: download from ', since, ori_df.iloc[-1])
        last_ts = 0
        while True:
            ohlcv = FTXApi.get_ohlc(perp_name, str(minutes)+'m', since)
            if len(ohlcv) > 0:
                df = pd.DataFrame(ohlcv)
                all_df = pd.concat([all_df[:-1],df])
                since = ohlcv[-1][0]
                if last_ts != ohlcv[-1][0]:
                    last_ts = ohlcv[-1][0]
                else:
                    break
            else:
                break
            time.sleep(0.2)
        all_df.columns = ['ts','open','high','low','close','volume']
        all_df = all_df.sort_values('ts', ascending=True)
        all_df = all_df.reset_index(drop=True)
        updated_df = pd.concat([ori_df[:-1], all_df[:-1]])
        updated_df = updated_df.sort_values('ts', ascending=True)
        updated_df = updated_df.reset_index(drop=True)
        print('added ', len(all_df)-1, ' data.')
        print(updated_df)
        file_name = perp_name+'-'+str(minutes) +'mcp'+'.csv'
        updated_df.to_csv('./Data/'+file_name)
        cls.checkDataFile(file_name)



    '''
    FTXのデータがTVでも抜けている箇所がある。
    '''
    @classmethod
    def checkDataFile(cls, file_name):
        df = cls.readOhlcvFile(file_name)
        print('duplicated ts=', (df['ts'].duplicated()).sum())
        num_skipped = 0
        ts = list(df['ts'])
        for i in range(len(ts)-1):
            if ts[i+1] - ts[i] != 60000:
                num_skipped+=1
        print('num skipped=', num_skipped)


    '''
    FTXのperp全銘柄の過去xヶ月分の時間足を取得する。
    '''
    @classmethod
    def GetAllData(cls, num_months):
        num_loop = int(round(num_months / 2.0))
        FTXApi.initialize()
        futures = FTXApi.get_future()
        futures=futures[(futures['type']=='perpetual')].reset_index()
        futures.to_csv('./Data/future-list.csv')
        j = 0
        for name in futures['name']:
            since = int(time.time()- (60 * 1500 * 60))*1000 #FTXのsinceは通常のtimestamp * 1000単位
            i = 0
            df = pd.DataFrame()
            all_df = pd.DataFrame()
            for i in range(num_loop):#1 loopでおよそ2ヶ月分の時間足を取得する
                li = FTXApi.get_ohlc(name, '1h', since)
                if len(li) > 0:
                    df = pd.DataFrame(li)
                    all_df = pd.concat([all_df,df])
                    since = int((since / 1000 - (60 * 1501 * 60))*1000) #1500本が最大取得可能なohlcv
                else:
                    break
            all_df.columns = ['ts','open','high','low','close','volume']
            all_df = all_df.sort_values('ts', ascending=True)
            all_df = all_df.reset_index(drop=True)
            print(j, '-', name, ' #', len(all_df))
            all_df.to_csv('./Data/'+name+'.csv')
        print('completed download all perp data.')


    '''
    1回で約1日分の分足を取得可能。
    since = num_months前のtsからデータ取得を開始する。
    31ヶ月が限界みたい。
    
    '''
    @classmethod
    def getMinutesMonthData(cls, minutes, num_months, perp_name):
        if minutes < 1:
            print('minutes should be larger than 1 !')
        if minutes > 60:
            print('minutes should be smaller than 60 !')
        else:
            print('Started download data')
            FTXApi.initialize()
            num_loop = int(round(num_months * ( 720.0 / (1500.0 / (60.0 / minutes))))) #1ヶ月（720時間）のデータを取得するのに何回ループが必要かという計算
            since = int(time.time() - 60 * 1440 * 30 * num_months) * 1000
            #since = int(time.time()- (int(minutes) * 1500))*1000 #FTXのsinceは通常のtimestamp * 1000単位
            df = pd.DataFrame()
            all_df = pd.DataFrame()
            i=0
            last_ts = 0
            while True:
                print(i, '/', num_loop, ':', datetime.fromtimestamp(int(since/1000)))
                ohlcv = FTXApi.get_ohlc(perp_name, str(minutes)+'m', since)
                if len(ohlcv) > 0:
                    df = pd.DataFrame(ohlcv)
                    all_df = pd.concat([all_df[:-1],df])
                    since = ohlcv[-1][0]
                    if last_ts != ohlcv[-1][0]:
                        last_ts = ohlcv[-1][0]
                    else:
                        break
                    time.sleep(0.2)
                else:
                    break
                i+=1
            all_df = all_df[:-1] #最後のデータはclose値が正しくないことがあるので捨てる
            all_df.columns = ['ts','open','high','low','close','volume']
            all_df = all_df.sort_values('ts', ascending=True)
            all_df = all_df.reset_index(drop=True)
            all_df.to_csv('./Data/'+perp_name+'-'+str(minutes) +'m'+'.csv')
            cls.checkDataFile(perp_name+'-'+str(minutes) +'m'+'.csv')
            return all_df
        print('Completed download data')



    @classmethod
    def readOhlcvFile(cls, file_name):
        df = pd.read_csv('./Data/'+file_name, index_col=0)
        return df


    @classmethod
    def readAllOhlcvFiles(cls):
        files = os.listdir('./Data')
        all_df = []
        for f in files:
            if '-PERP' in f:
                df = pd.read_csv('./Data/'+f,index_col=0)
                all_df.append(df)
        print('Completed read ' +str(len(all_df)) + ' data.' + ' size='+str(sys.getsizeof(all_df)))
        return all_df
    
    

if __name__ == '__main__':
    MarketData.getMinutesMonthData(1, 31, 'BTC-PERP')
    #df = MarketData.readOhlcvFile('BTC-PERP-1mcp.csv')
    #df[-41000:].to_csv('./Data/1-test.csv')
    #MarketData.addOhlcv(1, 'BTC-PERP')
    #MarketData.checkDataFile('BTC-PERP-1mcp.csv')

