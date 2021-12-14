
from openpyxl import load_workbook
import json



def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value



wb = load_workbook("PropPackConf.xlsx")
ws = wb.active

json_dir = "PropPackJson.json"

dic_parent = {}
row_index = 4
while ws.cell(row_index, 1).value != None:
    unit_dic = {}
    dic_parent.update({str(ws.cell(row_index,1).value): unit_dic})
    unit_dic.update({"id": ws.cell(row_index, 1).value})
    unit_dic.update({"type": ws.cell(row_index, 2).value})

    prop_list = []
    unit_dic.update({"prop_list": prop_list})
    for index in range(5):
        if ws.cell(row_index, 5+5*index).value !=None:
            dic_prop = {}

            dic_prop.update({"prop_id": ws.cell(row_index,5+5*index).value})
            dic_prop.update({"prop_num": ws.cell(row_index,6+5*index).value})
            dic_prop.update({"prop_type": ws.cell(row_index,7+5*index).value})
            dic_prop.update({"prop_color": ws.cell(row_index,8+5*index).value})

        prop_list.append(dic_prop)




    row_index = row_index + 1

    print("Complete Line : " + str(row_index))

with open(json_dir, "w") as json_file:
    json_str = json.dumps(dic_parent, indent=4)
    json_file.write(json_str)

