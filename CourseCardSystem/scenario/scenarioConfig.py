import xlwings as xw
import requests

# 1. 下载
# 2. 覆盖本地
# 3. 开始转换

# https://docs.google.com/spreadsheets/d/1enTwAruinyVWYAD8kGRwLu7cR8toyz6BoxOaE_awAhE/edit?usp=sharing
url_download = 'https://docs.google.com/spreadsheets/d/1enTwAruinyVWYAD8kGRwLu7cR8toyz6BoxOaE_awAhE/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('scenario.xlsx', 'wb').write(xlsx_file.content)


wb = xw.Book("scenario.xlsx")
ws1 = wb.sheets['Sheet1']

import json

# 支持输出中文

import os
work_dir = os.getcwd()
xlsx_dir = "scenario.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "upload.json"


json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)


# 工具
def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


result_dic = {}
hfc_chest_strategy = {}
result_dic.update({"hfc_chest_strategy": hfc_chest_strategy})

# 获取宝箱id
free_chest_id = int(ws1.range((2,3)).value)
sliver_chest_id = int(ws1.range((2,4)).value)
gold_chest_id = int(ws1.range((2,5)).value)
legen_chest_id = int(ws1.range((2,6)).value)


def dispose_config( chest_id, column_index):
    '''
    :param chest_id: 传入宝箱id
    :param column_index: 需要处理的列id
    '''
    row_start = 6
    chest_list = []
    hfc_chest_strategy.update({str(chest_id): chest_list})

    while ws1.range((row_start, column_index)).value != None:
        row_list = []
        chest_list.append(row_list)
        str_input = str(ws1.range((row_start, column_index)).value)
        str_input_list1 = str_input.split(";")
        for unit in str_input_list1:
            dic_add = {}
            input_list2 = unit.split(",")
            card_id = int(input_list2[0])
            card_num = int(input_list2[1])
            dic_add.update({"card_id": card_id})
            dic_add.update({"card_num": card_num})

            row_list.append(dic_add)

        row_start = row_start + 1

    print("宝箱 [ " + str(chest_id) + " ] 剧本配置完毕")



dispose_config(free_chest_id, 3)
dispose_config(sliver_chest_id, 4)
dispose_config(gold_chest_id, 5)
dispose_config(legen_chest_id, 6)





with open(json_dir, "w") as json_file:
    json_str = json.dumps(result_dic, indent=4)
    json_file.write(json_str)



