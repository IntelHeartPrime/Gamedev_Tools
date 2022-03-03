# 按行逐个读取csv
# 对各个用户的行为进行数据处理，并写于另一csv中
# output_csv  user_id, tag1,tag2,tag3,tag4...
# 之后使用SQL 的group by功能对其output_csv 进行相关分析
# 用Python处理 csv的速度是如此之快

import os
import csv

csv_file_path = "data_doubleBallOffer.csv"

# read csv

user_id_list = []

user_type_list = []

user_id_series_list = []


with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)

    index = 0
    for row in f_csv:
        # read csv successful
        if index > 0:
            user_id_cache = row[0]
            user_type_cache = row[4]
            user_series_tag = row[3]

            last_index = len(user_id_list) - 1

            #如果值不重复，则添加用户id
            if (last_index) >= 0:
                if(user_id_list[last_index] != user_id_cache):

                    user_id_list.append(user_id_cache)
                    user_type_list.append(user_type_cache)


                    empty_list = []
                    empty_list.append(user_series_tag)
                    user_id_series_list.append(empty_list)


                    # 为特定empty_list 中添加付费序列
                else:
                    last_index_user_id_serises_list = len(user_id_series_list) - 1
                    user_id_series_list[last_index_user_id_serises_list].append(user_series_tag)

            else:
                # 第一次添加用户id
                user_id_list.append(user_id_cache)
                empty_list = []
                empty_list.append(user_series_tag)
                user_id_series_list.append(empty_list)
                user_type_list.append(user_type_cache)

        index = index + 1

# 去掉纯免费玩家

paied_user_id_list = []
paied_user_type_list = []
paied_series_list = []

max_len = len(user_id_list)
for x in range(max_len):

    test_list = user_id_series_list[x]
    is_paied_player = False
    for tag_value in test_list:
        if tag_value == "gift1" or tag_value == "gift2" or tag_value == "gift3" or tag_value == "gift4" or \
                tag_value == "gift5":
            is_paied_player = True

    if is_paied_player:
        paied_user_id_list.append(user_id_list[x])
        paied_user_type_list.append(user_type_list[x])
        paied_series_list.append(test_list)

print(paied_series_list)

'''
# 计算所有包含gift1 的人   最后应输出 ： 6192 人

statistics_gift1 = 0

max_len = len(user_id_list)
for x in range(max_len):

    add_value = 0
    test_list = user_id_series_list[x]
    print("统计id = " + str(user_id_list[x]) + " 序列 = " + str(test_list))
    for tag_value in test_list:
        if tag_value == "gift1":
            add_value = 1
    statistics_gift1 = statistics_gift1 + add_value

print("statistics_gift1 = " + str(statistics_gift1))
'''


# 统计总数据数量
total_cnt = 0
for x in range(len(user_id_list)):
    for tag_value in user_id_series_list[x]:
        total_cnt = total_cnt + 1

print("total_cnt = " + str(total_cnt))

'''
# 处理数据1
data_result = []

for x in range(len(user_id_list)):
    line_unit = []
    line_unit.append(user_id_list[x])
    line_unit.append(user_type_list[x])

    for tag_value in user_id_series_list[x]:
        line_unit.append(tag_value)

    # 如果长度不够，则填充""
    while len(line_unit) < 23:
        line_unit.append("")

    data_result.append(line_unit)


# 开始写入csv
with open("output_data.csv", "w", newline= "" ) as f:
    ff = csv.writer(f)
    header = ["user_id", "user_type"]
    for x in range(21):
        header.append("tag" + str(x))
    ff.writerow(header)
    ff.writerows(data_result)

'''


# 处理数据2  - 只计算付费玩家
data_result = []

for x in range(len(paied_user_id_list)):
    line_unit = []
    line_unit.append(paied_user_id_list[x])
    line_unit.append(paied_user_type_list[x])

    tag_str = ""
    index = 0
    for tag_value in paied_series_list[x]:
        if index == 0:
            tag_str = tag_str + str(tag_value)
        else:
            tag_str = tag_str + "-" + str(tag_value)
        index = index + 1
    line_unit.append(tag_str)

    data_result.append(line_unit)


# 开始写入csv
with open("output_data_paid_player.csv", "w", newline= "" ) as f:
    ff = csv.writer(f)
    header = ["user_id", "user_type" ,"tag"]

    ff.writerow(header)
    ff.writerows(data_result)




with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)

    gift1_cnt = 0
    gift2_cnt = 0
    gift3_cnt = 0
    gift4_cnt = 0
    gift5_cnt = 0

    for row in f_csv:
        if row[3] == "gift1":
            gift1_cnt = gift1_cnt + 1
        if row[3] == "gift2":
            gift2_cnt = gift2_cnt+ 1
        if row[3] == "gift3":
            gift3_cnt = gift3_cnt+ 1
        if row[3] == "gift4":
            gift4_cnt = gift4_cnt+ 1
        if row[3] == "gift5":
            gift5_cnt = gift5_cnt+ 1

    print("gift1 = " + str(gift1_cnt))
    print("gift2 = " + str(gift2_cnt))
    print("gift3 = " + str(gift3_cnt))
    print("gift4 = " + str(gift4_cnt))
    print("gift5 = " + str(gift5_cnt))


# TODO add cdate tag  ex: day1-free, day1-token ....

