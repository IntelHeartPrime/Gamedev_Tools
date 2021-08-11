from openpyxl import load_workbook
import json

import os
work_dir = os.getcwd()
xlsx_dir = "CraneOfferconfigs.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "CraneOfferConfig.json"
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



container_dic = {}

# 总配置
container_dic.update({"id": ws.cell(4, 2).value})
container_dic.update({"name": ws.cell(5, 2).value})
container_dic.update({"coin_rate": ws.cell(6, 2).value})
container_dic.update({"start_time": ws.cell(7, 2).value})
container_dic.update({"end_time": ws.cell(8, 2).value})
container_dic.update({"begin_time": ws.cell(9, 2).value})
container_dic.update({"refresh_interval": ws.cell(10, 2).value})

# 小奖励配置
ticket_conf_list = []
container_dic.update({"ticket_conf_list": ticket_conf_list})

for x in range(3):
    if (ws.cell(17,1+x*10).value!= None):
        diff = x*10
        ticket_conf_list_unit_dic = {}
        ticket_conf_list_unit_dic.update({"min_stage": ws.cell(14,2+diff).value})
        ticket_conf_list_unit_dic.update({"max_stage": ws.cell(14,9+diff).value})

        ticket_levels_list = []
        ticket_conf_list_unit_dic.update({"ticket_levels": ticket_levels_list})
        row_index = 17
        while ws.cell(row_index,1).value!= None:
            ticket_levels_unit_dict = {}
            ticket_levels_unit_dict.update({"level": ws.cell(row_index, 1+diff).value})
            ticket_levels_unit_dict.update({"min": ws.cell(row_index, 2+diff).value})
            ticket_levels_unit_dict.update({"max": ws.cell(row_index, 3+diff).value})
            ticket_levels_unit_dict.update({"grade": ws.cell(row_index, 4+diff).value})

            reward_dic = {}
            ticket_levels_unit_dict.update({"reward": reward_dic})

            reward_dic.update({"prop_type": ws.cell(row, 5+diff).value})
            reward_dic.update({"prop_id": ws.cell(row, 6+diff).value})
            reward_dic.update({"prop_num": ws.cell(row, 7+diff).value})
            reward_dic.update({"prop_color": ws.cell(row, 8+diff).value})
            reward_dic.update({"chest_type": ws.cell(row, 9+diff).value})

            ticket_levels_list.append(ticket_levels_unit_dict)

            row_index = row_index + 1
        ticket_conf_list.append(ticket_conf_list_unit_dic)


# 大奖励配置
big_reward_list = []
container_dic.update({"big_reward_list": big_reward_list})

for x in range(3):
    if(ws.cell(60,1+x*10).value!= None):
        diff = x*10
        big_reward_list_unit_dic = {}

        big_reward_list_unit_dic.update({"min_stage": ws.cell(56, 2+diff).value})
        big_reward_list_unit_dic.update({"max_stage": ws.cell(56, 6+diff).value})

        big_rewards_list = []
        big_reward_list_unit_dic.update({"big_rewards": big_rewards_list})
        row_index = 60
        while ws.cell(row_index,1).value!= None:
            big_reward_unit_dic = {}
            big_reward_unit_dic.update({"unlock_level": ws.cell(row_index,1+diff).value})

            reward_dic = {}
            reward_dic.update({"prop_type": ws.cell(row, 2+diff).value})
            reward_dic.update({"prop_id": ws.cell(row, 3+diff).value})
            reward_dic.update({"prop_num": ws.cell(row, 4+diff).value})
            reward_dic.update({"prop_color": ws.cell(row, 5+diff).value})
            reward_dic.update({"chest_type": ws.cell(row, 6+diff).value})

            big_reward_unit_dic.update({"reward": reward_dic})

            big_rewards_list.append(big_reward_unit_dic)

            row_index = row_index + 1

        big_reward_list.append(big_reward_list_unit_dic)


# offer配置

offer_list =[]
container_dic.update({"offer_list": offer_list})

row_index = 80
while ws.cell(row_index, 1).value!= None:
    offer_list_unit_dic = {}
    offer_list_unit_dic.update( {"type": ws.cell(row_index, 1).value})
    offer_list_unit_dic.update( {"offer_id": ws.cell(row_index, 2).value})
    offer_list_unit_dic.update( {"consume_type": ws.cell(row_index, 3).value})
    offer_list_unit_dic.update( {"consume_num": ws.cell(row_index, 4).value})

    reward_list = []
    offer_list_unit_dic.update({"reward_list": reward_list})

    for x in range(3):
        while ws.cell(row_index, 5+x*5).value!= None:
            diff = x*5
            reward_list_unit_dic = {}
            reward_list_unit_dic.update({"prop_type": ws.cell(row_index, 5+diff)})
            reward_list_unit_dic.update({"prop_id": ws.cell(row_index, 6+diff)})
            reward_list_unit_dic.update({"prop_num": ws.cell(row_index, 7+diff)})
            reward_list_unit_dic.update({"prop_color": ws.cell(row_index, 8+diff)})
            reward_list_unit_dic.update({"chest_type": ws.cell(row_index, 9+diff)})

            reward_list.append(reward_list_unit_dic)

    offer_list.append(offer_list_unit_dic)

    row_index = row_index + 1


# UI相关配置

# ticket_reward_bg_list

















