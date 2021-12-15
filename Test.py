import datetime
import time
import os
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


# upbit = pyupbit.Upbit(access, secret)
# to의 형식 : "2021-11-04 10:00:00"
# 날짜에 따라 폴더를 생성하고 데이터를 저장함.
# 데이터는 1분 봉의 형태로 가지고 옴.

def coins_date_update(to):
    dir_name = to[0:10]
    os.makedirs(dir_name, exist_ok=True)
    coin_list = Quotation.tickers_list()
    for coin in coin_list:
        data = (pyupbit.get_ohlcv(ticker=coin, count=1440, interval="minute1", to="2021-11-04 10:00:00"))
        file_name = coin + "_" + str(datetime.datetime.today().day) + ".pkl"
        data.to_pickle(dir_name + '/' + file_name)
        time.sleep(0.2)


# 현재 날짜부터 원하는 일, 달, 또는 년도까지의 데이터를 싸그리 불러옴.
def update_database(day, month, year):
    date = datetime.datetime.now()
    while date.year == 2021:
        time = str(date)[0:10] + " 24:00:00"
        coins_date_update(time)
        date -= datetime.timedelta(days=1)


# 데이터들은 날짜별로 명명된 폴더에 저장되어 있음.
# 그 폴더의 이름을 만들어주는 역할을 함.
def make_date(day, month, year):
    if day // 10 == 0:
        day = '0' + str(day)
    else:
        day = str(day)
    date = str(year) + '-' + str(month) + '-' + day
    return date


path = make_date(5, 11, 2021)
path += '/KRW-BTC_5.pkl'


# data should be Series type, Pandas
# 코인들 데이터들 중에서 각각의 시간대에 따른 변동률을 계산함.
# 시간대인 인덱스도 나누어주어야 할 거 같은데?
def calculate_diff_ratio(data):
    diff = data['high'] / data['open'] - 1
    ratio = diff * 100
    return ratio


# os.chdir(path)로 이미 해당 폴더로 이동한 상태라고 가정함.
def back_testing(benchmark):
    result_filename = str(datetime.datetime.today())[0:10] +"_" + str(benchmark)
    f = open(result_filename+"txt", 'w')
    files_list = os.listdir()
    for file in files_list:
        if '.pkl' in file:
            data = pd.read_pickle(file)
            for i in range(len(data)):
                ratio = calculate_diff_ratio(data.iloc[i])
                if ratio > benchmark:
                    content = str(data.iloc[i].name) + " " + file[4:-6] +" " + str(ratio)
                    f.write(content)
                    f.write('\n')
    f.write('------------------------------------------------------')
    f.close()

os.chdir('2021-11-05')
back_testing(3)

