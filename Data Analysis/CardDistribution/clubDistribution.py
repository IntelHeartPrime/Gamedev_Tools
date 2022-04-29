
import xlwings as xw

wb = xw.Book("clubDistribution.xlsx")
ws1 = wb.sheets['sheet1']

cards = [1,2,6,16,36,86,186,386,786,1586,2586,4586,9586,19586,39586,79586,100000, 200000,300000]

def retrun_card_level_value( now_cards_sum ):
    '''
    :param now_cards_sum:  卡牌总张数
    :return:  返回一个float，代表其数值
    '''

    if now_cards_sum < 1:
        now_cards_sum = 1
    for x in range(len(cards)):
        if x < (len(cards)):
            left_value = cards[x]
            right_value = cards[x+1]

            print("x = " + str(x))
            print("now_card_sum = " + str(now_cards_sum) + " left_value =" + str(left_value) + " right_value = " \
                  + str(right_value) )
            if now_cards_sum >= left_value and now_cards_sum < right_value:
                diff_value = now_cards_sum - left_value
                progress_value = diff_value / ( right_value - left_value)

                result = x+1+progress_value

                return  result

row_index = 2580
while row_index  <= 30000:
    if (ws1.range((row_index, 13)).value) != None:
        result_value = retrun_card_level_value(ws1.range((row_index, 13)).value)
        ws1.range((row_index, 14)).value = result_value

        print("处理第 " + str(row_index) + " 数据 结果 = " + str(result_value))

    row_index = row_index + 1