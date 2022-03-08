
# HomeFieldConfig 配置转换

# 奖SkillConfig 从Excel转化为 Json

import xlwings as xw
import requests

'''
# 1. 下载
# 2. 覆盖本地
# 3. 开始转换

url_download = 'https://docs.google.com/spreadsheets/d/1y5lsly6S_ELAoXatQEurS-g_Tt9C80qxZCXthsevAzs/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('CourseCardConfig.xlsx', 'wb').write(xlsx_file.content)
'''

wb = xw.Book("HomeFieldConfig.xlsx")
ws1 = wb.sheets['Sheet1']
wsPVE = wb.sheets['pve']
wsPVP = wb.sheets['pvp']
wsReward = wb.sheets['reward_config']

import json

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


row_index = 3

HomeFieldConfig_list = []

while ws1.range((row_index,4)).value != None:
    unit_dic_inner = {}
    HomeFieldConfig_list.append(unit_dic_inner)

    unit_dic_inner.update({"id": int(ws1.range((3, 2)).value)})
    unit_dic_inner.update({"name": ws1.range((4, 2)).value})
    unit_dic_inner.update({"show_time_start": ws1.range((5, 2)).value})
    unit_dic_inner.update({"show_time_end": ws1.range((6, 2)).value})

    unit_dic_inner.update({"start_time": ws1.range((8, 2)).value})
    unit_dic_inner.update({"end-time": ws1.range((9, 2)).value})

    dic_unlock_condition = {}
    unit_dic_inner.update({"unlock_conditions": dic_unlock_condition})
    dic_unlock_condition.update({"stage": ws1.range((12,2)).value})

    # signup_offer_list
    sign_offer_list_dic = {}
    unit_dic_inner.update({"sign_offer_list": sign_offer_list_dic})

    pve_list = []
    pvp_list = []

    sign_offer_list_dic.update({"pve": pve_list})
    sign_offer_list_dic.update({"pvp": pvp_list})

    pay_rank_index = 0

    while ws1.range((pay_rank_index*7 + 2, 2).value) != None:
        

    ## pve config


    ## pvp config


    unit_dic_inner.update({"type": int(ws1.range((row_index, 7)).value)})
    unit_dic_inner.update({"color": int(ws1.range((row_index, 8)).value)})
    unit_dic_inner.update({"wind_min": int(ws1.range((row_index, 9)).value)})
    unit_dic_inner.update({"wind_max": int(ws1.range((row_index, 10)).value)})
    unit_dic_inner.update({"debuff_k": ws1.range((row_index, 11)).value})
    unit_dic_inner.update({"needle_speed_K": ws1.range((row_index, 12)).value})
    unit_dic_inner.update({"hole": int(ws1.range((row_index, 13)).value)})
    unit_dic_inner.update({"hole_size": ws1.range((row_index, 14)).value})
    unit_dic_inner.update({"par_dis": ws1.range((row_index, 15)).value})
    unit_dic_inner.update({"eagle_dis": ws1.range((row_index, 16)).value})
    unit_dic_inner.update({"flag_bounce": ws1.range((row_index, 17)).value})
    unit_dic_inner.update({"camera_height": int(ws1.range((row_index, 21)).value)})


    # Config ability # Waiting..
    ability_list = []
    unit_dic_inner.update({"ability": ability_list})

    # 获取 Ability 的索引列
    card_row_index = int(ws1.range((row_index, 18)).value)
    print(" card_row_index = " + str(card_row_index))
    while ws2.range((card_row_index, 1)).value != None:
        dic_ability = {}
        ability_list.append(dic_ability)

        dic_ability.update({"level": int(ws2.range((card_row_index, 1)).value)})
        dic_ability.update({"max_star": int(ws2.range((card_row_index, 2)).value)})
        dic_ability.update({"update_card": int(ws2.range((card_row_index, 3)).value)})
        dic_ability.update({"update_price": int(ws2.range((card_row_index, 4)).value)})
        dic_ability.update({"provide_exp": int(ws2.range((card_row_index, 5)).value)})
        dic_ability.update({"tee": int(ws2.range((card_row_index, 6)).value)})
        dic_ability.update({"par": int(ws2.range((card_row_index, 7)).value)})

        skills_list = []
        dic_ability.update({"skills": skills_list})
        ability_column_start_index = 8
        while ws2.range((card_row_index,ability_column_start_index )).value != None:
            skills_list.append(int(ws2.range((card_row_index, ability_column_start_index)).value))
            ability_column_start_index = ability_column_start_index + 1

        scene_show_dic = {}
        dic_ability.update({"scene_show_dic" : scene_show_dic})
        scene_show_dic.update({"show_prefab": ws2.range((card_row_index, 15)).value})
        path_pos_list = []
        scene_show_dic.update({"path_pos": path_pos_list})

        # path_pos 解析字符串  (a,b),(b,c),(c,d)...
        string_path_pos = str(ws2.range((int(card_row_index), 16)).value)
        path_pos_list_cache = ParsingStringPathPos(string_path_pos)

        for unit in path_pos_list_cache:
            path_pos_dic = {}
            float_x = unit[0]
            float_y = unit[1]
            path_pos_dic.update({"x": float_x})
            path_pos_dic.update({"y": float_y})
            path_pos_list.append(path_pos_dic)
        card_row_index = card_row_index + 1


    # config card_stage_infos
    # 获取其card_stage_infos 的索引列

    card_stage_infos_list = []
    unit_dic_inner.update({"card_stage_infos": card_stage_infos_list})

    info_row_index = int(ws1.range((row_index, 19)).value)
    print("info_row_index = " + str(info_row_index))
    while ws3.range((info_row_index, 1)).value != None:
        card_stage_dic ={}
        card_stage_infos_list.append(card_stage_dic)
        start_pos = {}
        card_stage_dic.update({"start_pos": start_pos})
        x_value = ws3.range((info_row_index, 2)).value
        y_value = ws3.range((info_row_index, 3)).value
        start_pos.update({"x": x_value})
        start_pos.update({"y": y_value})

        evaluation_rule_list = []
        card_stage_dic.update({"evaluation_rule": evaluation_rule_list})

        # evaluation_rule list添加
        # 获取 列索引
        column_start_index_str = int(ws3.range((info_row_index, 4)).value)
        split_column_start_index_str = column_start_index_str.split(',')

        row_start_index = split_column_start_index_str[0]
        column_start_index = split_column_start_index_str[1]
        print("行索引 = " + str(row_start_index) +" 列索引 = " + str(column_start_index))
        evaluation_row_index = row_start_index
        print("ws4中 行 = " + str(evaluation_row_index) + " 列 = " + str(column_start_index) + " 的值 = ")
        print("[ " + str(ws4.range((evaluation_row_index,column_start_index)).value) + " ]")
        while ws4.range((evaluation_row_index,column_start_index)).value != None:
            print("开始处理 evaluation_rule...")
            evaluation_list = []
            star_value = int(ws4.range((evaluation_row_index, column_start_index)).value)
            par_value = int(ws4.range((evaluation_row_index, column_start_index+1)).value)
            dis_value = int(ws4.range((evaluation_row_index, column_start_index+2)).value)

            evaluation_list = [star_value, par_value, dis_value]

            evaluation_rule_list.append(evaluation_list)
            print("行" + str(evaluation_row_index) + "，" + "列 " + str(column_start_index))
            evaluation_row_index = evaluation_row_index + 1


        info_row_index = info_row_index + 1

    # last
    row_index = row_index + 1



with open(json_dir, "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)



