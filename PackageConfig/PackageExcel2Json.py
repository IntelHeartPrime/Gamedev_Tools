
from openpyxl import load_workbook
import json



def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value



wb = load_workbook("e2j.xlsx")
ws = wb.active

json_dir = "Excel_to_Json.json"

unit_dic = {}
unit_dic.update({"id": clean_null(ws.cell(2,2).value)})
unit_dic.update({"show_time_start": clean_null(ws.cell(3,2).value)})
unit_dic.update({"start_time": clean_null(ws.cell(4,2).value)})
unit_dic.update({"show_time_end": clean_null(ws.cell(5,2).value)})
unit_dic.update({"end_time": clean_null(ws.cell(6,2).value)})
unit_dic.update({"join_before_end_time": clean_null(ws.cell(7,2).value)})
min_level = {}
unit_dic.update({"unlock_conditions": min_level})
min_level.update({"min_level": clean_null(ws.cell(8,4).value)})



with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)

