import datetime
import time
import os
import pandas as pd
import pyupbit
import Quotation
import shutil

pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

f = open("key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)


# to의 형식 : "2021-11-04 24:00:00"
# 날짜에 따라 폴더를 생성하고 데이터를 저장함.
# 데이터는 1분 봉의 형태로 가지고 옴.

def coins_date_update(to):
    dir_name = to[0:10]
    os.makedirs(dir_name, exist_ok=True)
    coin_list = Quotation.tickers_list()
    while coin_list == None:
        coin_list = Quotation.tickers_list()
        print("연결이 좀")
        time.sleep(0.2)
    for coin in coin_list:
        data = pyupbit.get_ohlcv(ticker=coin, count=200, interval="minute1", to=to)
        if data is None:
            continue
        # print(data)
        file_name = coin + ".pkl"
        data.to_pickle(dir_name + '/' + file_name)
        time.sleep(0.2)


# 현재 날짜부터 원하는 일, 달, 또는 년도까지의 데이터를 싸그리 불러옴.
def update_database():
    date = datetime.datetime(2021, 5, 8)
    while date.year == 2021:
        time1 = str(date)[0:10] + " 12:00:00"
        coins_date_update(time1)
        date -= datetime.timedelta(days=1)


update_database()


# 데이터들은 날짜별로 명명된 폴더에 저장되어 있음.
# 그 폴더의 이름을 만들어주는 역할을 함.
def make_date(day, month, year):
    if day // 10 == 0:
        day = '0' + str(day)
    else:
        day = str(day)
    date = str(year) + '-' + str(month) + '-' + day
    return date


def key_function(string):
    return int(string[11:13]) * 3600 + int(string[14:16]) * 60 + int(string[17:19])


# data should be Series type, Pandas
# 코인들 데이터들 중에서 각각의 시간대에 따른 변동률을 계산함.
# 시간대인 인덱스도 나누어주어야 할 거 같은데?
def calculate_diff_ratio(data):
    diff = data['high'] / data['open'] - 1
    ratio = diff * 100
    return ratio


def decompress_time_to_index(time):
    year = time[0:4]
    month = time[5:7]
    day = time[8:10]
    hour = time[11:13]
    minute = time[14:16]
    second = time[17:19]
    return year, month, day, hour, minute, second


# 급상승시간대, 코인, 판매비율 상하, 산 뒤 들고있는 최대 시간
# 날짜 기반으로 폴더 들어간 뒤 코인 파일을 엶.
# 시간대 이후로 가격 상하 조사 후 팔 수 있을 때 팔거임.
# 이 때 맥시멈 타임에서 지났는지 안 지났는지 검사
# 팔 수 있으면 팔 수 있는 시간, 가격
# 실패한 경우 -> 시간이 지남, 손해보고 팔았음 2가지 정도?
# while문 써서 인덱스 찾고 인덳스에서 분 시간을 1분씩 늘릴거임.

def investigation(time, coin, benchmark, up_sell_rate=5, down_sell_rate=5, maximum_time):
    dir_name = time[0:10]
    data = pd.read_pickle(dir_name+'/'+'KRW-'+coin+'.pkl')
    initial_index = datetime.datetime(decompress_time_to_index(time))
    starting_point = data.loc[initial_index]['open']*(1+benchmark/100)
    up_selling_point = starting_point*(1+up_sell_rate/100)
    down_selling_point = starting_point*(1-down_sell_rate/100)
    end_index = initial_index + datetime.timedelta(hours=maximum_time)
    for



# os.chdir(path)로 이미 해당 폴더로 이동한 상태라고 가정함.
# 벤치마크보다 높이 오른 코인들, 시간대를 계산함
# 시간대순으로 정렬해줌.
def back_testing_step_1(benchmark, folder_name):
    os.chdir(folder_name)
    result_filename = os.getcwd() + "_" + str(benchmark) + ".txt"
    f = open(result_filename, 'w')
    files_list = os.listdir()
    for file in files_list:
        if '.pkl' in file:
            data = pd.read_pickle(file)
            for i in range(len(data)):
                ratio = calculate_diff_ratio(data.iloc[i])
                if ratio > benchmark:
                    content = str(data.iloc[i].name) + " " + file[4:-6] + " " + str(ratio)
                    f.write(content)
                    f.write('\n')
    f.close()
    os.chdir('C:\\Users\\조성민\\PycharmProjects\\Upbit')
    with open('2021-11-05_4.txt', 'r') as f:
        list = f.readlines()
        list.sort(key=key_function)
    with open('2021-11-05_4.txt', 'w') as f:
        f.writelines(list)


#
def back_testing_step_2(result_file_of_the_day):
    coin_list = []
    with open(result_file_of_the_day) as result:
        the_increased_times = result.readlines()
        for data in the_increased_times:
            coin = data[21:-18]
            the_increased_time = data[0:20]
            if coin not in coin_list:
                coin_list.append((the_increased_time, coin))
    for inc_time, coin in coin_list:
        investigation(inc_time, coin, buy_rate=5, sell_rate=5, maximum_time=3)

