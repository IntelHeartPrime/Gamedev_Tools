# 输入：剧本string list
'''
str = [
    "8,1;3,6;4,2",
    "4,4;5,1;8,10",
    "3,16;6,15"
        ]
'''

# 输出 不同步骤下各个卡片等级
'''
out = [ 
    ["card1", "card2", ....],
    [0,1,...],
    [....],
    ...
     ]
'''


input_str = [
    "8,1;3,6;4,2",
    "4,4;5,1;8,10",
    "3,16;6,15"
        ]


list_table_head = []
for x in range(8):
    list_table_head.append("card" + str(x+1))
print("list_table_head = " + list_table_head)

# creat dic
dic_card_num = {}
for x in list_table_head:
    dic_card_num.update({"str(x)": 0})


# 传入card_id & card_now_num,输出等级
def get_card_level( card_now_num):
    '''
    :param card_now_num: 卡片目前总数量
    :return: card_level
    '''
    card_upgrade_list = [0, 5, 10, 20, 30, 50, 80, 120, 170, 230]
    for x in range(len(card_upgrade_list)):
        if card_now_num >= card_upgrade_list[x] and card_now_num <= card_upgrade_list[x+1]:
            
for str_unit in input_str:
    str_unit_split1 = str(str_unit).split(";")
    list_time = []
    for str_unit_split2 in str_unit_split1:
        card_id = str_unit_split2[0]
        card_num = str_unit_split2[1]
        for x in range(1, 9):
            if x == int(card_id):
                card_now_num = dic_card_num["card" + str(x)] + card_num
                dic_card_num["card" + str(x)] = card_now_num

                # 将card_now_num 转化为等级


