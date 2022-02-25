# 奖SkillConfig 从Excel转化为 Json

import xlwings as xw
wb = xw.Book("KingdomSimulator.xlsx")
ws1 = wb.sheets['Sheet1']
ws2 = wb.sheets['ability1']
ws3 = wb.sheets['cardstageinfo1']
ws4 = wb.sheets['evaluation_rule']


import json
import re

# 支持输出中文

import os
work_dir = os.getcwd()
xlsx_dir = "CourseCardConfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "CourseCardConfig.json"

json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)

# 工具

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


row_index = 5

unit_dic = {}

while ws1.range((row_index,4)).value != None:
    unit_dic_inner = {}
    unit_dic.update({ws1.range((row_index,1)).value: unit_dic_inner})
    unit_dic_inner.update({"id": ws1.range((row_index, 1)).value})
    unit_dic_inner.update({"name": ws1.range((row_index, 2)).value})
    unit_dic_inner.update({"scene_name": ws1.range((row_index, 3)).value})
    unit_dic_inner.update({"icon_small": ws1.range((row_index, 4)).value})
    unit_dic_inner.update({"icon_big": ws1.range((row_index, 5)).value})
    unit_dic_inner.update({"atlas_name": ws1.range((row_index, 6)).value})
    unit_dic_inner.update({"type": ws1.range((row_index, 7)).value})
    unit_dic_inner.update({"color": ws1.range((row_index, 8)).value})
    unit_dic_inner.update({"wind_min": ws1.range((row_index, 9)).value})
    unit_dic_inner.update({"wind_max": ws1.range((row_index, 10)).value})
    unit_dic_inner.update({"debuff_k": ws1.range((row_index, 11)).value})
    unit_dic_inner.update({"needle_speed_K": ws1.range((row_index, 12)).value})
    unit_dic_inner.update({"hole": ws1.range((row_index, 13)).value})
    unit_dic_inner.update({"hole_size": ws1.range((row_index, 14)).value})
    unit_dic_inner.update({"par_dis": ws1.range((row_index, 15)).value})
    unit_dic_inner.update({"eagle_dis": ws1.range((row_index, 16)).value})
    unit_dic_inner.update({"flag_bounce": ws1.range((row_index, 17)).value})


    # Config ability # Waiting..

    ability_list = []
    # 获取其card_stage_infos 的索引列
    card_row_index = ws1.range((row_index, 18)).value
    while ws2.range((card_row_index, 1)).value != None:
        dic_ability = {}
        dic_ability.update({"level": ws2.range((card_row_index, 1)).value})
        dic_ability.update({"max_star": ws2.range((card_row_index, 2)).value})
        dic_ability.update({"update_card": ws2.range((card_row_index, 3)).value})
        dic_ability.update({"update_price": ws2.range((card_row_index, 4)).value})
        dic_ability.update({"provide_exp": ws2.range((card_row_index, 5)).value})
        dic_ability.update({"tee": ws2.range((card_row_index, 6)).value})
        dic_ability.update({"par": ws2.range((card_row_index, 7)).value})

        skills_list = []
        dic_ability.update({"skills": skills_list})
        ability_column_start_index = 8
        while ws2.range((card_row_index, 8)).value != None:
            skills_list.append(ws2.range((card_row_index, 8)).value)
            ability_column_start_index = ability_column_start_index + 1

        scene_show_dic = {}
        dic_ability.update({"scene_show_dic" : scene_show_dic})
        scene_show_dic.update({"show_prefab": ws2.range((card_row_index, 15)).value})
        path_pos_list = []
        scene_show_dic.update({"path_pos": path_pos_list})

        # path_pos 解析字符串  (a,b),(b,c),(c,d)...
        # use Python findall













    row_index = row_index + 1


with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)




