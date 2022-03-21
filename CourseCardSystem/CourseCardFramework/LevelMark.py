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

row_start = 5
while ws1.range((row_start, 3)).value != None:
    chapter_id = ws1.range((row_start, 1)).value
    level_id = ws1.range((row_start, 2)).value
    card_string = ws1.range((row_start, 3)).value
    card_lv = ws1.range((row_start, 4)).value
    print(" chapter_id = " + str(chapter_id) + " level = " + str(level_id) + " 场景 = " + str(card_string) + \
          " 场景等级 = " + str(card_lv))

    row_start = row_start + 1




