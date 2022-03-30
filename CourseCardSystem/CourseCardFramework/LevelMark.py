'''

xlwings set cell color : sht.range('A6:V10').color = (255,0,0)

Legendary : 255,130,171
Epic: 132,112,255
Rare: 255,165,79

'''

import xlwings as xw
import requests
import string

wb = xw.Book("CourseCardSystemThink.xlsx")
ws1 = wb.sheets['Dungeon']


# row = 5  column = 3
# 卡片库 row = 30 column 13 ~ 20
dic_cardDepository = {}
dic_cardDepository.update({"橙1": 14})
dic_cardDepository.update({"橙2": 15})
dic_cardDepository.update({"紫1": 16})
dic_cardDepository.update({"紫2": 17})
dic_cardDepository.update({"紫3": 18})
dic_cardDepository.update({"紫4": 19})
dic_cardDepository.update({"传奇1": 20})
dic_cardDepository.update({"传奇2": 21})

dic_cardLevelProgress = {}
dic_cardLevelProgress.update({"橙1": 23})
dic_cardLevelProgress.update({"橙2": 24})
dic_cardLevelProgress.update({"紫1": 25})
dic_cardLevelProgress.update({"紫2": 26})
dic_cardLevelProgress.update({"紫3": 27})
dic_cardLevelProgress.update({"紫4": 28})
dic_cardLevelProgress.update({"传奇1": 29})
dic_cardLevelProgress.update({"传奇2": 30})


dic_color = {}
dic_color.update({"橙1": (255,165,79)})
dic_color.update({"橙2": (255,165,79)})
dic_color.update({"紫1": (132,112,255)})
dic_color.update({"紫2": (132,112,255)})
dic_color.update({"紫3": (132,112,255)})
dic_color.update({"紫4": (132,112,255)})
dic_color.update({"传奇1": (255,130,171)})
dic_color.update({"传奇2": (255,130,171)})

dic_nowLevel = {}
dic_nowLevel.update({"橙1": 0})
dic_nowLevel.update({"橙2": 0})
dic_nowLevel.update({"紫1": 0})
dic_nowLevel.update({"紫2": 0})
dic_nowLevel.update({"紫3": 0})
dic_nowLevel.update({"紫4": 0})
dic_nowLevel.update({"传奇1": 0})
dic_nowLevel.update({"传奇2": 0})


# 关卡颜色清零

origin_color = ws1.range((1,1)).color

row_start = 5
while ws1.range((row_start, 3)).value != None:
    ws1.range((row_start, 3)).color = origin_color
    row_start = row_start + 1

# 球场卡库颜色清零
for col in range(13, 20):
    for row in range(31, 41):
        ws1.range((row, col)).color  = origin_color

row_start = 5
while ws1.range((row_start, 3)).value != None:
    chapter_id = int(ws1.range((row_start, 1)).value)
    level_id = int(ws1.range((row_start, 2)).value)
    card_string = ws1.range((row_start, 3)).value
    card_lv = int(ws1.range((row_start, 4)).value)
    print(" chapter_id = " + str(chapter_id) + " level = " + str(level_id) + " 场景 = " + str(card_string) + \
          " 场景等级 = " + str(card_lv))

    # 遍历字典，获取目标颜色
    for key_str in dic_color.keys():
        if card_string == key_str:
            ws1.range((row_start, 3)).color = dic_color[key_str]
            break

    # 标记球场卡库
    col_index = dic_cardDepository[card_string]
    row_index_cardDepository = 30 + card_lv
    ws1.range((row_index_cardDepository, col_index)).color = dic_color[key_str]

    # 对传奇卡张数的解析
    # col = 11 是传奇卡的阵列
    legen_card = ""
    legen_card_lv = 0

    if ws1.range((row_start, 11)).value != None:
        # 开始解析传奇卡
        legen_card_str = str(ws1.range((row_start, 11)).value)
        legen_card_str_list = legen_card_str.split("-")
        # 去空格
        legen_card = legen_card_str_list[0].strip()

        # 解析等级
        legen_card_str_lv = legen_card_str.split("Lv")
        # 得等级
        legen_card_lv = int(legen_card_str_lv[len(legen_card_str_lv)-1])



    # 列出所有进度需要的卡片等级
    for key_str in dic_nowLevel.keys():

        # 紫卡和橙卡
        if card_string == key_str:
            # 判断等级大小
            now_level = dic_nowLevel[key_str]
            if card_lv >= now_level:
                dic_nowLevel[key_str] = card_lv
                print("  Update - 卡片【" + str(card_string) + "】 当前最高等级 = " + str(card_lv))
        else:
            print("  Keep - 卡片【" + str(key_str) + "】 当前最高等级 = " + str(dic_nowLevel[key_str]))
        # 紫卡和橙卡

        # 传奇卡
        if legen_card == key_str:
            # 判断等级大小
            now_level = dic_nowLevel[key_str]
            if legen_card_lv >= now_level:
                dic_nowLevel[key_str] = legen_card_lv
                print("  传奇卡 Update - 卡片【" + str(legen_card) + "】 当前最高等级 = " + str(legen_card_lv))
        else:
            print("  传奇卡 Keep - 卡片【" + str(key_str) + "】 当前最高等级 = " + str(dic_nowLevel[key_str]))
        # 传奇卡


    for key_str in dic_cardLevelProgress.keys():
        col_level_index = dic_cardLevelProgress[key_str]
        ws1.range((row_start, col_level_index)).value = dic_nowLevel[key_str]
        print(" 行 = " + str(row_start) + " 列 = " + str(col_level_index) + " 的值设置为 [" + str(dic_nowLevel[key_str]) + "]")


    row_start = row_start + 1


