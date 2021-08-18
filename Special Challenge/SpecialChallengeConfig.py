from openpyxl import load_workbook
import json

import os
work_dir = os.getcwd()
xlsx_dir = "SpcecialChallengeconfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "SpeicalChallengeConfig.Json"
json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)

wb = load_workbook(workbook_dir)
ws = wb.active

# 工具

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


def get_bool(input_string):
    '''
    input_string = "true" return true
    input_string = "false" return false
    '''
    if input_string == "true":
        return True
    elif input_string == "false":
        return  False
    else:
        return  False

container_dic = {}

#总配置
container_dic.update({"name": ws.cell(3, 2).value})
container_dic.update({"id": ws.cell(4, 2).value})
container_dic.update({"start_time": ws.cell(5, 2).value})
container_dic.update({"end_time": ws.cell(6, 2).value})
container_dic.update({"chance": ws.cell(8, 2).value})
container_dic.update({"chance_fee": ws.cell(9, 2).value})
container_dic.update({"diamond_offer_trigger_num": ws.cell(10, 2).value})

# 限定配置
battle_limit ={}
container_dic.update({"battle_limit": battle_limit})

balls = []
battle_limit.update({"balls": balls})
column_index = 2
while ws.cell(15, column_index).value!= None:
    balls.append(ws.cell(15, column_index).value)
    column_index = column_index + 1

club_color = []
battle_limit.update({"club_color": club_color})
column_index = 2
while ws.cell(19, column_index).value!= None:
    club_color.append(ws.cell(19, column_index).value)
    column_index = column_index + 1

clubs = []

