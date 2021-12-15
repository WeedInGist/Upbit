import pyupbit


# 업비트 서버에 접속해서 온갖 종류의 데이터들을 내가 원하는 형태로 가공할지
# 아니면 그냥 데이터들을 한번 쭉 가져와서 내가 알아서 가공할지
# 아마도 후자로 하는 것이 훨씬 나을 것임.


f = open("key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)

def tickers_list(fiat="KRW"):
    tickers = pyupbit.get_tickers(fiat=fiat)
    while tickers is None:
        tickers = pyupbit.get_tickers(fiat=fiat)
        print("와이파이가 끊어져서 코인 리스트 뽑는 과정 재시도중")
    return tickers


# 인수로 넘어가는 값에 따라서 시장의 코인들을 전부 리스트로 반환


def how_many_differences(ticker_bought, ticker_bought_price):
    current_price = pyupbit.get_current_price(ticker_bought)
    while current_price is None:
        current_price = pyupbit.get_current_price(ticker_bought)
        print("코인 현재가 가져오는 중에 연결 끊어져서 재시도중1")
    per = 100 * current_price / ticker_bought_price - 100
    return per


# 내가 산 코인과 그 가격을 넣으면 현재 수익률을 알려줌


def more_than_zero_list(rate=0.0):
    potential_list = []
    tickers = tickers_list()
    for ticker in tickers:
        data = pyupbit.get_ohlcv(ticker, interval="minute10")
        while data is None:
            data = pyupbit.get_ohlcv(ticker, interval="minute10")
        open_price = data.iloc[-1]['open']
        current_price = data.iloc[-1]['close']
        per = 100 * current_price / open_price - 100
        if per >= rate:
            potential_list.append((per, ticker))
    return potential_list.sort()
# rate 비율보다 높이 오른 코인들을 리스트로 반환




