import json
import os
import xlwings as xw # xlwings库的使用方法暗要额外注意

# 工具函数

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


def print_list(input_list):
    str_out =""
    for x in input_list:
        str_out = str_out + str(x)
    return str_out


# 配置路径

work_dir = os.getcwd()

wb= xw.Book("Props_config.xlsx")
ws = wb.sheets['Sheet1']
ws_out = wb.sheets['Sheet2']


row_start = 3
while ws.range((row_start, 1)).value != None:
    tour_id = int(ws.range((row_start, 1)).value)
    course_id = int(ws.range((row_start, 2)).value)
    column_start = 4
    club_ids1 = []
    club_levels1 = []

    club_ids2 = []
    club_levels2 = []


    # 数据采集
    for x in range(11):
        if ws.range((row_start, x*5 +column_start + 1)).value != None:

            # 判断第一杆
            same_value_cnt = 0
            club_id = int(ws.range((row_start, x * 5 + column_start + 1)).value)
            club_level = int(ws.range((row_start, x * 5 + column_start + 2)).value)

            for id in club_ids1:
                if id == club_id:
                    same_value_cnt = same_value_cnt + 1

            if same_value_cnt == 0:
                club_ids1.append(club_id)
                club_levels1.append(club_level)

                print("此杆第一杆场需要杆: " + str(club_id) + " Lv = " + str(club_level))

        if ws.range((row_start, x * 5 + column_start + 3)).value != None:

            # 判断第二杆
            same_value_cnt = 0
            club_id = int(ws.range((row_start, x * 5 + column_start + 3)).value)
            club_level = int(ws.range((row_start, x * 5 + column_start + 4)).value)

            for id in club_ids2:
                if id == club_id:
                    same_value_cnt = same_value_cnt + 1

            if same_value_cnt == 0:
                club_ids2.append(club_id)
                club_levels2.append(club_level)

                print("此杆第二杆场需要杆: " + str(club_id) + " Lv = " + str(club_level))

    # 完成数据采集

    # 写入数据
    ws_out.range((row_start, 1)).value = tour_id
    ws_out.range((row_start, 2)).value = course_id

    index = 0

    for x in range(len(club_ids1)):
        ws_out.range((row_start, 4+3*index)).value = club_ids1[x]
        ws_out.range((row_start, 5+3*index)).value = club_levels1[x]
        ws_out.range((row_start, 6+3*index)).value = "第一杆"

        index = index + 1

    for x in range(len(club_ids2)):
        ws_out.range((row_start, 4 + 3 * index)).value = club_ids2[x]
        ws_out.range((row_start, 5 + 3 * index)).value = club_levels2[x]
        ws_out.range((row_start, 6 + 3 * index)).value = "第二杆"

        index = index + 1


    print("完成一行")

    row_start = row_start + 1


