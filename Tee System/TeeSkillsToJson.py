from openpyxl import load_workbook
import json

import os
work_dir = os.getcwd()
xlsx_dir = "TeeConfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "TeeSkills.json"
json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)

wb = load_workbook(workbook_dir)
ws = wb.active



row_index = 5

dicts_list = []


while ws.cell(row_index,2).value != None:

    unit_dic = {}
    unit_dic.update({"skill_id": ws.cell(row_index, 2).value})
    unit_dic.update({"skill_level": ws.cell(row_index, 3).value})
    unit_dic.update({"match_type": ws.cell(row_index, 4).value})

    buff_list = []
    buff_dic = {}
    buff_dic.update({"type": ws.cell(row_index, 5).value})
    buff_dic.update({"rate": ws.cell(row_index, 6).value})
    buff_dic.update({"value": ws.cell(row_index, 7).value})

    buff_list.append(buff_dic)
    unit_dic.update({"buff_list" : buff_list})

    pirze_list = []
    prize_dict = {}

    prize_dict.update({"type": ws.cell(row_index,8).value})
    condition_list = []
    condition_list.append(ws.cell(row_index,9).value)
    condition_list.append(ws.cell(row_index,10).value)
    condition_list.append(ws.cell(row_index,11).value)
    condition_list.append(ws.cell(row_index,12).value)
    condition_list.append(ws.cell(row_index,13).value)
    prize_dict.update({"condition": condition_list})
    prize_dict.update(({"rate": ws.cell(row_index,14).value}))

    prize_dict.update(({"extra_trophy": ws.cell(row_index,15).value}))
    prize_dict.update(({"trophy_shield": ws.cell(row_index,16).value}))
    prize_dict.update(({"kingdom_extra_score": ws.cell(row_index,17).value}))
    prize_dict.update(({"kingdom_score_shield": ws.cell(row_index,18).value}))

    reward_list = []
    for x in range(6):
        if(ws.cell(row_index, 19+5*x).value != None) and (ws.cell(row_index, 19+x).value != ""):
            reward_dic = {}
            reward_dic.update({"prop_id": ws.cell(row_index, 19+5*x).value})
            reward_dic.update({"prop_type": ws.cell(row_index, 20+5*x).value})
            reward_dic.update({"prop_color": ws.cell(row_index, 21+5*x).value})
            reward_dic.update({"prop_num": ws.cell(row_index, 22+5*x).value})
            reward_dic.update({"chest_type": ws.cell(row_index, 23+5*x).value})
            reward_list.append(reward_dic)

    prize_dict.update({"reward_list" : reward_list})
    pirze_list.append(prize_dict)

    unit_dic.update({"prize_list": pirze_list})


    row_index = row_index + 1
    dicts_list.append(unit_dic)

with open(json_dir, "w") as json_file:
    index = 0
    for dict_unit in dicts_list:

        index = index + 1
        json_str = json.dumps(dict_unit, indent=4)
        if( index < len(dicts_list)):
            json_file.write(json_str + ",")
        else:
            json_file.write(json_str)
        json_file.write("\r")




