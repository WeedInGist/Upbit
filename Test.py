import datetime
import time

import pandas as pd
import pyupbit
import Quotation
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

f = open("key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)
# to의 형식 : "2021-11-04 10:00:00"
# 1분 봉의 형태로 가지고 옴.
def coins_date_update(to):
    coin_list =Quotation.tickers_list()
    for coin in coin_list:
        data = (pyupbit.get_ohlcv(ticker=coin, count=61, interval="minute1", to="2021-11-04 10:00:00"))
        file_name = coin+"_"+str(datetime.datetime.today().day)+".pkl"
        data.to_pickle(file_name)
        time.sleep(0.2)

coins_list = Quotation.tickers_list()
# 데이터파일 이름 만들기
