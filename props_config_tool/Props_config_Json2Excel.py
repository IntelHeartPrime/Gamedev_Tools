# 导入包
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

json_file_name = "Props_config.json"

data_object =[]

# 读取Json & 输出到 Excel
# 读取Json

with open(json_file_name) as json_file:
    data = json_file.read()
    data_object = json.loads(data)
    print(data_object)

# 遍历写入Excel

row_index= 1
for unit in data_object:

    ws.range((row_index, 2)).value = unit["course_id"]
    ws.range((row_index, 3)).value = unit["id"]

    props_list = unit["props"]
    column_index = 0
    for x in props_list:
        ws.range((row_index, 4+column_index*5)).value = print_list(x["balls"])
        clubs_list = x["clubs"]
        inner_index = 0
        for y in clubs_list:
            ws.range((row_index,5+column_index*5+inner_index*2)).value = y["id"]
            ws.range((row_index,6+column_index*5+inner_index*2)).value = y["level"]
            inner_index = inner_index+1
        column_index = column_index+1

    ws.range((row_index, 1)).value = unit["tour"]
    row_index = row_index + 1



