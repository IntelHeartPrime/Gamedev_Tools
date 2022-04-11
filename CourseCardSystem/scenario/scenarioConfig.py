import xlwings as xw
import requests

# 1. 下载
# 2. 覆盖本地
# 3. 开始转换

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

# 工具 解析字符串
def ParsingStringPathPos( path_pos_str ):
    '''
    :param path_pos_str: 输入的
    :return: 所有点的list - 输出值为float
    '''
    print(" 开始解析字符串 " + str(path_pos_str))
    result_list = []
    list_1 = path_pos_str.split("(")
    for unit_1 in list_1:
        list_2 = unit_1.split(")")
        for unit_2 in list_2:
            list_3 = unit_2.split(",")
            if (list_3[0] != ""):
                list_append = [ float(list_3[0]), float(list_3[1])]
                result_list.append(list_append)
    print(" 解析路径数据后 " + str(result_list))
    return result_list



row_index = 6

unit_dic = {}




with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)



