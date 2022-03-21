'''

xlwings set cell color : sht.range('A6:V10').color = (255,0,0)

Legendary : 255,130,171
Epic: 132,112,255
Rare: 255,165,79

'''



import xlwings as xw
import requests
wb = xw.Book("CourseCardSystemThink.xlsx")
ws1 = wb.sheets['Dungeon']


# row = 5  column = 3
# 卡片库 row = 30 column 13 ~ 20
dic_cardDepository = {}
dic_cardDepository.update({"橙1": 13})
dic_cardDepository.update({"橙2": 14})
dic_cardDepository.update({"紫1": 15})
dic_cardDepository.update({"紫2": 16})
dic_cardDepository.update({"紫3": 17})
dic_cardDepository.update({"紫4": 18})
dic_cardDepository.update({"传奇1": 19})
dic_cardDepository.update({"传奇2": 20})

dic_color = {}
dic_color.update({"橙1": (255,165,79)})
dic_color.update({"橙2": (255,165,79)})
dic_color.update({"紫1": (132,112,255)})
dic_color.update({"紫2": (132,112,255)})
dic_color.update({"紫3": (132,112,255)})
dic_color.update({"紫4": (132,112,255)})
dic_color.update({"传奇1": (255,130,171)})
dic_color.update({"传奇2": (255,130,171)})

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

    
    row_start = row_start + 1





