# 奖SkillConfig 从Excel转化为 Json

from openpyxl import load_workbook
import json

# 支持输出中文

import os
work_dir = os.getcwd()
xlsx_dir = "SkillConfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "skillConfig.json"
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


row_index = 3

unit_dic = {}

while ws.cell(row_index,4).value != None:
    unit_dic_inner = {}
    unit_dic.update({str(ws.cell(row_index, 4).value): unit_dic_inner})
    unit_dic_inner.update({"Note": clean_null(str(ws.cell(row_index, 5).value))})
    unit_dic_inner.update({"skill_id": ws.cell(row_index, 6).value})
    unit_dic_inner.update({"skill_type": clean_null(ws.cell(row_index, 7).value)})
    unit_dic_inner.update({"skill_desc": clean_null(ws.cell(row_index, 8).value)})
    unit_dic_inner.update({"skill_value": clean_null(ws.cell(row_index, 9).value)})


    row_index = row_index + 1


with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)




