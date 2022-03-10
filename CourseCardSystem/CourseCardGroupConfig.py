# 奖SkillConfig 从Excel转化为 Json

import xlwings as xw
import requests

# 1. 下载
# 2. 覆盖本地
# 3. 开始转换

url_download = 'https://docs.google.com/spreadsheets/d/1wo9ct33xEV0QaiR3c2_U5Ew30WBxpUF8p6Be6wuYR6o/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('CourseCardGroupConfig.xlsx', 'wb').write(xlsx_file.content)

wb = xw.Book("CourseCardGroupConfig.xlsx")
ws = wb.sheets['Sheet1']

import json

# 支持输出中文

import os
work_dir = os.getcwd()

json_file_name = "CourseCardGroupConfig.json"

json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)


# 工具

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


row_index = 4

unit_dic = {}

while ws.range((row_index,1)).value != None:
    unit_dic_inner = {}
    unit_dic.update({int(ws.range((row_index,1)).value): unit_dic_inner})
    unit_dic_inner.update({"id": int(ws.range((row_index, 1)).value)})
    unit_dic_inner.update({"name": ws.range((row_index, 2)).value})
    unit_dic_inner.update({"is_active": ws.range((row_index, 3)).value})

    course_card = []
    unit_dic_inner.update({"course_cards" : course_card})

    column_index_start = 4
    while ws.range((row_index, column_index_start)).value != None:
        unit_dic_add= {}
        unit_dic_add.update({"id": int(ws.range((row_index, column_index_start)).value)})
        course_card.append(unit_dic_add)
        column_index_start = column_index_start + 1

    row_index = row_index + 1
    print("输出第 " + str(row_index)+ " 行数据")


with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)

    print("Group 配置完毕")




