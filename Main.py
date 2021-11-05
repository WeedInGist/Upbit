import Trading
import Quotation
import datetime
import time

num_of_coins_to_buy = 5


def main():
    if num_of_coins_to_buy % 2 == 0:
        high_position = num_of_coins_to_buy // 2
        low_position = num_of_coins_to_buy - high_position
    else:
        high_position = (num_of_coins_to_buy + 1) // 2
        low_position = num_of_coins_to_buy - high_position

    while True:
        now = datetime.datetime.now()
        if now.hour >= 9:
            time.sleep(20)
            zero_list_sorted = Quotation.more_than_zero_list(0.0)
            for i in range(high_position):
                Trading.buy_order_immediately(zero_list_sorted[-i-2])
            for i in range(low_position):
                Trading.buy_order_immediately(zero_list_sorted[i])
        # 이젠 산 것들 조회하면서 -20퍼 내려간 것만 팔거임 get_balances 활용
        # 계속 가격 비교하면서 평단가 비교하다가 20퍼, -20퍼에 매도주문



main()
