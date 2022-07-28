# 奖SkillConfig 从Excel转化为 Json

import xlwings as xw
import requests

# 1. 下载
# 2. 覆盖本地
# 3. 开始转换

url_download = 'https://docs.google.com/spreadsheets/d/1SIcCTEro3ea7NjZwF8jOE8PGL_7BWR0a8261sUiZIxg/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('LuckySpinConfig.xlsx', 'wb').write(xlsx_file.content)

wb = xw.Book("LuckySpinConfig.xlsx")
wsC = wb.sheets['Config']

#stage_l = ["s9", "s10"]
stage_l = ["s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17", "s18", "s19"]

import json

# 支持输出中文

import os
work_dir = os.getcwd()
json_file_name = "luckySpinConfig.json"
json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)

# 工具

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value

''' 总配置结构 '''
dic_Parent = {}

dic_Parent.update({"id": int(wsC.range((3, 2)).value)})
dic_Parent.update({"name": wsC.range((4, 2)).value})
dic_Parent.update({"start_time": int(wsC.range((5, 2)).value)})
dic_Parent.update({"end_time": int(wsC.range((6, 2)).value)})
dic_Parent.update({"unlock_stage": int(wsC.range((7, 2)).value)})
dic_Parent.update({"grand_prize_Index": int(wsC.range((8, 2)).value)})
dic_Parent.update({"reset_pop_up_interval": int(wsC.range((9, 2)).value)})
dic_Parent.update({"shards_ep": int(wsC.range((9, 2)).value)})

spin_update_mins = []
dic_Parent.update({"spin_update_mins": spin_update_mins})
col_start =2
while wsC.range((12, col_start)).value != None:
    spin_update_mins.append(int(wsC.range((12, col_start)).value))
    col_start += 1

reset_consume = []
dic_Parent.update({"reset_consume": reset_consume})
col_start = 2
while wsC.range((16, col_start)).value != None:
    dic = {}
    dic.update({"consume_type": int(wsC.range((16, col_start)).value)})
    dic.update({"consume_num": int(wsC.range((17, col_start)).value)})
    reset_consume.append(dic)

    col_start += 1

spin_consume = []
dic_Parent.update({"spin_consume": spin_consume})

spin_weight = []
dic_Parent.update({"spin_weight": spin_weight})

item = []
dic_Parent.update({"item": item})

box = []
dic_Parent.update({"box": box})

ad_config = {}
dic_Parent.update({"ad_config": ad_config})


''' spin_consume '''
def SpinConsumeConfig( sheet_name, container):
    '''
    :param sheet_name: 所在的sheet_name
    :param container: 数据容器 - list
    :return: None
    '''

    ws1 = wb.sheets[str(sheet_name)]
    dic = {}
    container.append(dic)

    stage_index = int(ws1.range((3,2)).value)

    dic.update({"stage": stage_index})
    consume = []
    dic.update({"consume": consume})

    for x in range(2, 10):
        dic_inner = {}
        dic_inner.update({"need_hole_num": int(ws1.range((6, x)).value)})
        dic_inner.update({"consume_type": int(ws1.range((7, x)).value)})
        dic_inner.update({"consume_num": int(ws1.range((8, x)).value)})

        consume.append(dic_inner)

    print(" stage " + str(stage_index) + " spin_consume config completed")

'''spin_weight'''
def SpinWeightConfig():

    for r in range(23, 30+1):
        item_weight = []
        for c in range(2, 9+1):
            item_weight.append(int(wsC.range((r, c)).value))

        spin_weight.append(item_weight)

    print(" spin_weight complete")

'''item'''
def ItemConfig( sheet_name, container):
    '''
    :param sheet_name: 所在的sheet_name
    :param container: 数据容器 - list
    :return: None
    '''

    ws1 = wb.sheets[str(sheet_name)]
    dic = {}
    container.append(dic)

    stage_index = int(ws1.range((3,2)).value)
    dic.update({"stage": stage_index})

    item_pool = []
    dic.update({"item_pool": item_pool})

    for x in range(1, 8+1):

        print(" stage " + str(stage_index) + " 第" + str(x) + " 个奖池")
        pool = []
        item_pool.append(pool)
        row_start = 29
        while ws1.range((row_start, 1)).value != None:
            if int(ws1.range((row_start, 1)).value) == x:
                dic_inner = {}
                prop = {}
                dic_inner.update({"prop": prop})
                prop.update({"prop_id": int(ws1.range((row_start, 3)).value)})
                prop.update({"prop_type": int(ws1.range((row_start, 4)).value)})
                prop.update({"prop_color": int(ws1.range((row_start, 5)).value)})

                dic_inner.update({"weight": int(ws1.range((row_start, 7)).value)})
                dic_inner.update({"max_num": int(ws1.range((row_start, 8)).value)})
                dic_inner.update({"min_num": int(ws1.range((row_start, 9)).value)})

                pool.append(dic_inner)

            row_start += 1

    print(" stage " + str(stage_index) + " item config completed")

'''box'''
def BoxConfig(sheet_name, container):
    '''
    :param sheet_name: 所在的sheet_name
    :param container: 数据容器
    :return: None
    '''
    ws1 = wb.sheets[str(sheet_name)]
    dic = {}
    container.append(dic)

    stage_index = int(ws1.range((3,2)).value)
    dic.update({"stage": stage_index})

    box_list = []
    dic.update({"box_list": box_list})
    col_start = 2
    while ws1.range((15, col_start)).value != None:
        dic_inner = {}
        box_list.append(dic_inner)

        dic_inner.update({"need_spin_times": int(ws1.range((15, col_start)).value)})
        reward = {}
        dic_inner.update({"reward": reward})
        reward.update({"prop_id": int(ws1.range((18, col_start)).value)})
        reward.update({"prop_num": int(ws1.range((19, col_start)).value)})
        reward.update({"prop_type": int(ws1.range((20, col_start)).value)})
        reward.update({"prop_color": int(ws1.range((21, col_start)).value)})
        reward.update({"chest_type": int(ws1.range((22, col_start)).value)})

        col_start += 1

    print("stage" + str(stage_index) + " box config completed")

''' ad_config '''
def AdConfig():
    ad_config.update({"ad_enable": int(wsC.range((35, 2)).value)})
    ad_config.update({"ln_a": wsC.range((36, 2)).value})
    ad_config.update({"ln_b": wsC.range((37, 2)).value})

    ln_area_min = {}
    ad_config.update({"ln_area_min": ln_area_min})
    ln_area_min.update({"value": wsC.range((40, 2)).value})
    ln_area_min.update({"rate": wsC.range((41, 2)).value})

    ln_area_max = {}
    ad_config.update({"ln_area_max": ln_area_max})
    ln_area_max.update({"value": wsC.range((44, 2)).value})
    ln_area_max.update({"rate": wsC.range((45, 2)).value})

    stage_list = []
    ad_config.update({"stage_list": stage_list})

    col_start = 2
    while wsC.range((48, col_start)).value != None:
        dic = {}
        stage_list.append(dic)
        dic.update({"stage": int(wsC.range((48, col_start)).value)})
        dic.update({"adjust": wsC.range((49, col_start)).value})
        dic.update({"window_min": wsC.range((50, col_start)).value})
        dic.update({"window_max": wsC.range((51, col_start)).value})

        col_start += 1

    print(" ad_config complete")



''' 按照模块逐步生成配置数据 '''
for s in stage_l:
    SpinConsumeConfig(s, spin_consume)

SpinWeightConfig()

for s in stage_l:
    ItemConfig(s, item)

for s in stage_l:
    BoxConfig(s, box)

AdConfig()

with open(json_dir, "w") as json_file:
    json_str = json.dumps(dic_Parent, indent=4)
    json_file.write(json_str)



