import Quotation
import pyupbit

f = open("key.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)
balance = upbit.get_balance("KRW") / 10005 *99



def sell_order_immediately():
    info = upbit.sell_market_order(ticker_bought, upbit.get_balance(ticker_bought))
    """
    print(ticker_bought + " 팔았음 이윤은 " + str(per) + "%")
    logging.info("%s 팔았습니다.", ticker_bought)
    logging.info("이윤은 %s 입니다", str(per))
    """
    return info


def buy_order_immediately(ticker, money = balance):
    info = upbit.buy_market_order(ticker, money)
    """
    buy_time = datetime.datetime.now()
    logging.info("%s 때 들어갔습니다.", per)
    logging.info("%s 샀습니다.", ticker)
    """
    return info

