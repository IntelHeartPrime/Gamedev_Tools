# HomeFieldConfig 配置转换

# 奖SkillConfig 从Excel转化为 Json

import xlwings as xw
import requests

# 1. 下载
# 2. 覆盖本地
# 3. 开始转换
url_download = 'https://docs.google.com/spreadsheets/d/1qRCofncJSH2bKQtcnMSfFoqHHhRE3OEUzscD2A9M-HQ/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('HomeFieldConfig.xlsx', 'wb').write(xlsx_file.content)

wb = xw.Book("HomeFieldConfig.xlsx")
ws1 = wb.sheets['Sheet1']
wsPVE = wb.sheets['pve']
wsPVP = wb.sheets['pvp']
wsReward = wb.sheets['reward_config']

import json

import os

work_dir = os.getcwd()
xlsx_dir = "HomeFieldConfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "HomeFieldConfig.json"

# leave here
json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)


# 工具
def clean_null(input_value):
    empty_value = ""
    if input_value is None:
        return empty_value
    return input_value

# 工具—判断是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

# 工具 解析字符串
def ParsingStringPathPos(path_pos_str):
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
                list_append = [float(list_3[0]), float(list_3[1])]
                result_list.append(list_append)
    print(" 解析路径数据后 " + str(result_list))
    return result_list


row_index = 3

HomeFieldConfig_list = []

# dic

unit_dic_inner = {}
HomeFieldConfig_list.append(unit_dic_inner)

unit_dic_inner.update({"id": int(ws1.range((3, 2)).value)})
unit_dic_inner.update({"game_id": int(ws1.range((13, 2)).value)})


# color tours
color_tours_list = []
unit_dic_inner.update({"color_tours": color_tours_list})
column_index_start = 2
while ws1.range((107, column_index_start)).value != None:
    dic = {}
    dic.update({"color": int(ws1.range((107, column_index_start)).value)})
    dic.update({"tour_id": int(ws1.range((108, column_index_start)).value)})

    color_tours_list.append(dic)

    column_index_start =column_index_start +1


unit_dic_inner.update({"name": ws1.range((4, 2)).value})
unit_dic_inner.update({"show_time_start": int(ws1.range((5, 2)).value)})
unit_dic_inner.update({"show_time_end": int(ws1.range((6, 2)).value)})

unit_dic_inner.update({"start_time": int(ws1.range((8, 2)).value)})
unit_dic_inner.update({"end_time": int(ws1.range((9, 2)).value)})

unit_dic_inner.update({"shop_coins_per_diamond": int(ws1.range((12, 4)).value)})
unit_dic_inner.update({"card_coins_per_diamond": int(ws1.range((12, 6)).value)})

dic_unlock_condition = {}
unit_dic_inner.update({"unlock_conditions": dic_unlock_condition})
dic_unlock_condition.update({"stage": int(ws1.range((12, 2)).value)})

# push & mail
push_dic = {}
unit_dic_inner.update({"push": push_dic})
push_dic.update({"end_content": ws1.range((91, 2)).value})
push_dic.update({"start_content": ws1.range((92, 2)).value})
push_dic.update({"on_hook_full_content": ws1.range((93, 2)).value})
push_dic.update({"refresh_ticket_content": ws1.range((94, 2)).value})
push_dic.update({"pvp_start_content": ws1.range((95, 2)).value})
push_dic.update({"push_before_end_minute": int(ws1.range((96, 2)).value)})

unit_dic_inner.update({"mail_title": ws1.range((100, 2)).value})
unit_dic_inner.update({"mail_content": ws1.range((101, 2)).value})



# signup_offer_list
sign_offer_list = []
unit_dic_inner.update({"signup_offer_list": sign_offer_list})

daily_boost_offer_row_start = 16
accelerate_offer_row_start = 25
ticket_offer_row_start = 34

def fill_offer_config( row_start ):

    global sign_offer_list
    '''
    :param row_start:  开始的行数
    '''
    unit_list = []
    sign_offer_list.append(unit_list)

    unit_dic = {}
    unit_list.append(unit_dic)



    unit_dic.update({"name" : ws1.range((row_start, 2)).value})
    unit_dic.update({"offer_type" : int(ws1.range((row_start+1, 2)).value)})
    unit_dic.update({"money" : int(ws1.range((row_start+2, 2)).value)})
    unit_dic.update({"type" : int(ws1.range((row_start+3, 2)).value)})

    unit_dic.update({"start_time" : int(ws1.range((row_start, 5)).value)})
    unit_dic.update({"refresh_time" : int(ws1.range((row_start+1, 5)).value)})
    unit_dic.update({"end_before" : int(ws1.range((row_start+2, 5)).value)})

    signup_offer_id_list = []
    unit_dic.update({"signup_offer_id_list" : signup_offer_id_list})

    column_index_start = 2
    while ws1.range((row_start + 5,column_index_start)).value != None:
        dic_add = {}
        dic_add.update({"money": ws1.range((row_start+5, column_index_start)).value})
        dic_add.update({"offer_id": int(ws1.range((row_start+6, column_index_start)).value)})

        signup_offer_id_list.append(dic_add)

        column_index_start = column_index_start + 1

    print("某一offer配置完成")

# fill_offer_config_separately
def fill_offer_config_separately( row_start ):

    global sign_offer_list
    '''
    :param row_start:  开始的行数
    '''
    unit_list = []
    sign_offer_list.append(unit_list)

    column_index_start = 2
    while ws1.range((row_start,column_index_start)).value != None:
        unit_dic = {}
        unit_list.append(unit_dic)

        unit_dic.update({"name" : ws1.range((row_start, column_index_start)).value})
        unit_dic.update({"offer_type" : int(ws1.range((row_start+1, column_index_start)).value)})
        unit_dic.update({"money" : int(ws1.range((row_start+2, column_index_start)).value)})
        unit_dic.update({"type" : int(ws1.range((row_start+3, column_index_start)).value)})

        unit_dic.update({"start_time" : int(ws1.range((row_start+5, column_index_start)).value)})
        unit_dic.update({"refresh_time" : int(ws1.range((row_start+6, column_index_start)).value)})
        unit_dic.update({"end_before" : int(ws1.range((row_start+7, column_index_start)).value)})

        signup_offer_id_list = []
        unit_dic.update({"signup_offer_id_list" : signup_offer_id_list})

        dic_add = {}
        dic_add.update({"money": ws1.range((row_start+9, column_index_start)).value})
        dic_add.update({"offer_id": int(ws1.range((row_start+10, column_index_start)).value)})

        signup_offer_id_list.append(dic_add)

        column_index_start = column_index_start + 1

    print("某一offer配置完成")



fill_offer_config(daily_boost_offer_row_start)
fill_offer_config(accelerate_offer_row_start)
fill_offer_config_separately(ticket_offer_row_start)


'''
pve_list = []
pvp_list = []
tickets_list = []

sign_offer_list_dic.update({"pve": pve_list})
sign_offer_list_dic.update({"pvp": pvp_list})
sign_offer_list_dic.update({"tickets": tickets_list})

# pve_signup_offer
pay_rank_index = 0

while ws1.range((17, pay_rank_index * 7 + 2)).value != None:

    pve_dic = {}
    pve_list.append(pve_dic)
    pve_dic.update({"money": ws1.range((17, pay_rank_index * 7 + 2)).value})
    pve_dic.update({"type": int(ws1.range((18, pay_rank_index * 7 + 2)).value)})
    sign_offer_id_list = []
    pve_dic.update({"signup_offer_id_list": sign_offer_id_list})

    column_index = 0

    while ws1.range((20, pay_rank_index * 7 + 2 + column_index)).value != None:
        offer_id_list_dic = {}
        sign_offer_id_list.append(offer_id_list_dic)
        offer_id_list_dic.update({"money": ws1.range((20, pay_rank_index * 7 + 2 + column_index)).value})
        offer_id_list_dic.update({"offer_id": int(ws1.range((21, pay_rank_index * 7 + 2 + column_index)).value)})

        column_index = column_index + 1

    pay_rank_index = pay_rank_index + 1

# pvp_signup_offer

pay_rank_index = 0

while ws1.range((25, pay_rank_index * 7 + 2)).value != None:

    pvp_dic = {}
    pvp_list.append(pvp_dic)
    pvp_dic.update({"money": ws1.range((25, pay_rank_index * 7 + 2)).value})
    pvp_dic.update({"type": int(ws1.range((26, pay_rank_index * 7 + 2)).value)})
    sign_offer_id_list = []
    pvp_dic.update({"signup_offer_id_list": sign_offer_id_list})

    column_index = 0
    while ws1.range((28, pay_rank_index * 7 + 2 + column_index)).value != None:
        offer_id_list_dic = {}
        sign_offer_id_list.append(offer_id_list_dic)
        offer_id_list_dic.update({"money": ws1.range((28, pay_rank_index * 7 + 2 + column_index)).value})
        offer_id_list_dic.update({"offer_id": int(ws1.range((29, pay_rank_index * 7 + 2 + column_index)).value)})

        column_index = column_index + 1

    pay_rank_index = pay_rank_index + 1

# tickets_sign_up_offer


pay_rank_index = 0

while ws1.range((75, pay_rank_index * 7 + 2)).value != None:

    tickets_dic = {}
    tickets_list.append(tickets_dic)
    tickets_dic.update({"money": ws1.range((75, pay_rank_index * 7 + 2)).value})
    tickets_dic.update({"type": int(ws1.range((76, pay_rank_index * 7 + 2)).value)})
    tickets_dic.update({"cd": int(ws1.range((75, pay_rank_index * 7 + 4)).value)})
    tickets_dic.update({"open_time": int(ws1.range((75, pay_rank_index * 7 + 6)).value)})
    tickets_dic.update({"end_before": int(ws1.range((76, pay_rank_index * 7 + 6)).value)})

    sign_offer_id_list = []
    tickets_dic.update({"signup_offer_id_list": sign_offer_id_list})

    column_index = 0
    while ws1.range((78, pay_rank_index * 7 + 2 + column_index)).value != None:
        offer_id_list_dic = {}
        sign_offer_id_list.append(offer_id_list_dic)
        offer_id_list_dic.update({"money": ws1.range((78, pay_rank_index * 7 + 2 + column_index)).value})
        offer_id_list_dic.update({"offer_id": int(ws1.range((79, pay_rank_index * 7 + 2 + column_index)).value)})

        column_index = column_index + 1

    pay_rank_index = pay_rank_index + 1

'''


# course_level_upgrade_rules
course_level_upgrade_rules = []
unit_dic_inner.update({"course_level_upgrade_rules": course_level_upgrade_rules})
row_index = 61
while ws1.range((row_index, 1)).value != None:
    dic = {}
    dic.update({"level": int(ws1.range((row_index, 1)).value)})
    dic.update({"need_exp": int(ws1.range((row_index, 2)).value)})

    # 读取new_content，每次循环增加两列，直到为空
    new_content = []
    column_innner_index = 4
    while ws1.range((row_index, column_innner_index)).value is not None:
        title_dic = {}
        if isinstance(ws1.range((row_index,column_innner_index)).value, float):
            title = int(ws1.range((row_index,column_innner_index)).value)
            title_dic.update({"title": str(title)})
        else:
            title_dic.update({"title": str(ws1.range((row_index, column_innner_index)).value)})

        # 判断此值是否为数字
        transfer_value = str(ws1.range((row_index, column_innner_index + 1)).value)
        if is_number(transfer_value):
            title_dic.update({"value": int(ws1.range((row_index, column_innner_index + 1)).value)})
        else:
            title_dic.update({"value": ws1.range((row_index, column_innner_index + 1)).value})

        new_content.append(title_dic)
        column_innner_index = column_innner_index + 2
    dic.update({"new_content": new_content})

    # 读取rewards，每次循环增加6列，直到为空
    rewards = []
    column_innner_index = 11
    while ws1.range((row_index, column_innner_index)).value is not None:
        prop_dic = {}
        prop_dic.update({"prop_id": int(ws1.range((row_index, column_innner_index)).value)})
        prop_dic.update({"prop_num": int(ws1.range((row_index, column_innner_index + 1)).value)})
        prop_dic.update({"prop_type": int(ws1.range((row_index, column_innner_index + 2)).value)})
        prop_dic.update({"prop_color": int(ws1.range((row_index, column_innner_index + 3)).value)})
        prop_dic.update({"chest_type": int(ws1.range((row_index, column_innner_index + 4)).value)})
        rewards.append(prop_dic)
        column_innner_index = column_innner_index + 6
    dic.update({"rewards": rewards})

    course_level_upgrade_rules.append(dic)

    row_index = row_index + 1

print("courselevel 配置完成")


print("总览配置完成")

## pve config
pve_conf = {}
unit_dic_inner.update({"pve_conf": pve_conf})

pve_conf.update({"init_offer_chapter": int(wsPVE.range((3, 2)).value)})
pve_conf.update({"free_card": int(wsPVE.range((4, 2)).value)})
pve_conf.update({"on_hook_limit_time_sec": int(wsPVE.range((6, 2)).value)})
pve_conf.update({"on_hook_receive_limit_sec": int(wsPVE.range((8, 2)).value)})



on_hook_rule = []
row_index = 177
column_innner_index = 2
while wsPVE.range((row_index, column_innner_index)).value is not None:
    hook_rule_dic = {}
    hook_rule_dic.update({"star": int(wsPVE.range((row_index, column_innner_index)).value)})
    hook_rule_dic.update({"card_coin_per_sec": int(wsPVE.range((row_index + 1, column_innner_index)).value)})
    hook_rule_dic.update({"shop_coin_per_sec": int(wsPVE.range((row_index + 2, column_innner_index)).value)})
    on_hook_rule.append(hook_rule_dic)
    column_innner_index = column_innner_index + 1

pve_conf.update({"on_hook_rules": on_hook_rule})

# tickets_update_mins
tickets_update_mins = []
pve_conf.update({"tickets_update_mins": tickets_update_mins})
column_index = 2
while wsPVE.range((5, column_index)).value != None:
    tickets_update_mins.append(int(wsPVE.range((5, column_index)).value))
    column_index = column_index + 1

# shop_update_mins
shop_update_mins = []
pve_conf.update({"shop_update_mins": shop_update_mins})
column_index = 2
while wsPVE.range((5, column_index)).value != None:
    shop_update_mins.append(int(wsPVE.range((15, column_index)).value))
    column_index = column_index + 1


pve_conf.update({"default_tickets": int(wsPVE.range((7, 2)).value)})

tickets_shop = []
pve_conf.update({"tickets_shop": tickets_shop})
column_index = 2
while wsPVE.range((10, column_index)).value != None:
    dic = {}
    dic.update({"type": int(wsPVE.range((10, column_index)).value)})
    dic.update({"consume_num": int(wsPVE.range((11, column_index)).value)})
    dic.update({"consume_type": int(wsPVE.range((12, column_index)).value)})
    dic.update({"get_num": int(wsPVE.range((13, column_index)).value)})

    tickets_shop.append(dic)
    column_index = column_index + 1
# chapter_list

chapter_list = []

pve_conf.update({"chapter_list": chapter_list})

row_index = 23
while wsPVE.range((row_index, 1)).value != None:
    dic = {}
    chapter_list.append(dic)
    dic.update({"id": int(wsPVE.range((row_index, 1)).value)})
    dic.update({"name": wsPVE.range((row_index, 2)).value})

    level_id_list = str(wsPVE.range((row_index, 3)).value).split(',')
    print("-------------------------------------------------------")
    print("chapter config  id = " + str(int(wsPVE.range((row_index, 1)).value)))

    checkpoint = []
    dic.update({"checkpoint": checkpoint})
    for x in level_id_list:
        id = int(float(x))
        print(" id = " + str(id))
        row_start_index = 23
        while wsPVE.range((row_start_index, 6)).value != None:
            if id == int(wsPVE.range((row_start_index, 5)).value):
                # 读取此行数据作为奖励内容
                dic = {}

                print("     checkpoint config  id = " + str(int(wsPVE.range((row_start_index, 5)).value)))
                print("     row index = " + str(row_start_index))

                dic.update({"id": int(wsPVE.range((row_start_index, 6)).value)})
                dic.update({"scene_id": int(wsPVE.range((row_start_index, 7)).value)})
                dic.update({"side_story": int(wsPVE.range((row_start_index, 8)).value)})
                dic.update({"ticket_cost": int(wsPVE.range((row_start_index, 9)).value)})
                battle_limit = {}
                dic.update({"battle_limit": battle_limit})
                battle_limit.update({"home_field_level": int(wsPVE.range((row_start_index, 10)).value)})
                battle_limit.update({"star_limit": int(wsPVE.range((row_start_index, 11)).value)})
                dic.update({"level": int(wsPVE.range((row_start_index, 13)).value)})

                # basic rewards config
                basic_reward = []
                dic.update({"basic_reward": basic_reward})
                reward_id = int(wsPVE.range((row_start_index, 12)).value)

                reward_row_index = 3
                if_start_record = False

                while (wsReward.range((reward_row_index, 5)).value) != None:
                    if wsReward.range((reward_row_index, 1)).value != None:
                        if int(wsReward.range((reward_row_index, 1)).value) == reward_id:
                            # 从此处开始向下计算
                            if_start_record = True
                    if (if_start_record):
                        if (wsReward.range((reward_row_index, 1)).value != None) and \
                                (int(wsReward.range((reward_row_index, 1)).value) != reward_id):
                            break
                        else:
                            # 开始记录奖励
                            reward_dic = {}
                            basic_reward.append(reward_dic)

                            reward_dic.update({"star": int(wsReward.range((reward_row_index, 3)).value)})

                            reward = []
                            reward_dic.update({"reward": reward})

                            column_jump_id = 0
                            while wsReward.range((reward_row_index, column_jump_id * 7 + 4)).value != None:
                                dic_1 = {}
                                dic_1.update(
                                    {"prop_id": int(wsReward.range((reward_row_index, column_jump_id * 7 + 4)).value)})
                                dic_1.update(
                                    {"prop_num": int(wsReward.range((reward_row_index, column_jump_id * 7 + 5)).value)})
                                dic_1.update({"prop_type": int(
                                    wsReward.range((reward_row_index, column_jump_id * 7 + 6)).value)})
                                dic_1.update({"prop_color": int(
                                    wsReward.range((reward_row_index, column_jump_id * 7 + 7)).value)})
                                dic_1.update({"chest_type": int(
                                    wsReward.range((reward_row_index, column_jump_id * 7 + 8)).value)})

                                reward.append(dic_1)

                                column_jump_id = column_jump_id + 1

                    reward_row_index = reward_row_index + 1

                checkpoint.append(dic)
            row_start_index = row_start_index + 1

    row_index = row_index + 1
print("关卡与奖励配置完成 ")

# process_rewards
process_rewards = []
pve_conf.update({"process_rewards": process_rewards})

row_index_1 = 23
while wsPVE.range((row_index_1, 17)).value != None:
    dic = {}
    process_rewards.append(dic)

    dic.update({"star_num": int(wsPVE.range((row_index_1, 17)).value)})
    dic.update({"is_big_reward": int(wsPVE.range((row_index_1, 18)).value)})

    reward = {}
    dic.update({"reward": reward})
    reward.update({"prop_id": int(wsPVE.range((row_index_1, 19)).value)})
    reward.update({"prop_num": int(wsPVE.range((row_index_1, 20)).value)})
    reward.update({"prop_type": int(wsPVE.range((row_index_1, 21)).value)})
    reward.update({"prop_color": int(wsPVE.range((row_index_1, 22)).value)})
    reward.update({"chest_type": int(wsPVE.range((row_index_1, 23)).value)})

    row_index_1 = row_index_1 + 1

print("process_rewards 配置完成")


## pvp config

pvp_conf = {}
unit_dic_inner.update({"pvp_conf": pvp_conf})
pvp_conf.update({"start_time": int(wsPVP.range((4, 2)).value)})
pvp_conf.update({"end_time": int(wsPVP.range((5, 2)).value)})

battle_limit = {}
pvp_conf.update({"battle_limit": battle_limit})
battle_limit.update({"home_field_level": int(wsPVP.range((8, 2)).value)})
battle_limit.update({"star": int(wsPVP.range((9, 2)).value)})
pvp_conf.update({"select_cards_num": int(wsPVP.range((11,2)).value)})
row_pvp = 15

stage_conf = []
pvp_conf.update({'stage_conf': stage_conf})
while wsPVP.range((row_pvp, 1)).value != None:
    dic = {}
    dic.update({"id": int(wsPVP.range((row_pvp, 1)).value)})
    dic.update({"grade": int(wsPVP.range((row_pvp, 2)).value)})
    dic.update({"small_level": int(wsPVP.range((row_pvp, 3)).value)})
    dic.update({"upgrade_score": int(wsPVP.range((row_pvp, 4)).value)})
    dic.update({"home_field_level_remote_limit": int(wsPVP.range((row_pvp, 5)).value)})
    dic.update({"big_reward": int(wsPVP.range((row_pvp, 14)).value)})

    score_rules = {}
    dic.update({'score_rules': score_rules})
    score_rules.update({"big_win": int(wsPVP.range((row_pvp, 7)).value)})
    score_rules.update({"small_win": int(wsPVP.range((row_pvp, 8)).value)})
    score_rules.update({"mini_win": int(wsPVP.range((row_pvp, 9)).value)})
    score_rules.update({"draw": int(wsPVP.range((row_pvp, 10)).value)})
    score_rules.update({"mini_lose": int(wsPVP.range((row_pvp, 11)).value)})
    score_rules.update({"small_lose": int(wsPVP.range((row_pvp, 12)).value)})
    score_rules.update({"big_lose": int(wsPVP.range((row_pvp, 13)).value)})

    stage_conf.append(dic)

    reward = []
    dic.update({"reward": reward})

    column_jump = 0
    while (wsPVP.range((row_pvp, column_jump * 6 + 16)).value) != None:
        reward_dic = {}
        reward_dic.update({"prop_id": int(wsPVP.range((row_pvp, column_jump * 6 + 16)).value)})
        reward_dic.update({"prop_num": int(wsPVP.range((row_pvp, column_jump * 6 + 17)).value)})
        reward_dic.update({"prop_type": int(wsPVP.range((row_pvp, column_jump * 6 + 18)).value)})
        reward_dic.update({"prop_color": int(wsPVP.range((row_pvp, column_jump * 6 + 19)).value)})
        reward_dic.update({"chest_type": int(wsPVP.range((row_pvp, column_jump * 6 + 20)).value)})

        reward.append(reward_dic)

        column_jump = column_jump + 1
    row_pvp = row_pvp + 1

print("pvp配置完成")

# ui config
ui_config_dic = {}
unit_dic_inner.update({"ui_config": ui_config_dic})
ui_config_dic.update({"map_vrew_scale": 1.4})
print("ui_config配置完成")

store_box_list = []
unit_dic_inner.update({"store_box_list": store_box_list})
row_index_store = 53
while wsPVP.range((row_index_store, 1)).value != None:
    dic = {}
    dic.update({"pos": int(wsPVP.range((row_index_store, 1)).value)})
    dic.update({"consume_type": int(wsPVP.range((row_index_store, 2)).value)})
    dic.update({"consume_num": int(wsPVP.range((row_index_store, 3)).value)})

    chest_dic = {}
    chest_dic.update({"prop_id": int(wsPVP.range((row_index_store, 4)).value)})
    chest_dic.update({"prop_num": int(wsPVP.range((row_index_store, 5)).value)})
    chest_dic.update({"prop_type": int(wsPVP.range((row_index_store, 6)).value)})
    chest_dic.update({"prop_color": int(wsPVP.range((row_index_store, 7)).value)})
    chest_dic.update({"chest_type": int(wsPVP.range((row_index_store, 8)).value)})
    dic.update({"chest": chest_dic})
    store_box_list.append(dic)
    row_index_store = row_index_store + 1

with open(json_dir, "w") as json_file:
    json_str = json.dumps(HomeFieldConfig_list, indent=4)
    json_file.write(json_str)

