# 将文件从Club转换为Json

import os
import json
import xlwings as xw


''' 函数 输入文件名，数据容器类实例，生成相应Json'''

def Export2Json(fileName, dataContainer):
    with open(fileName+".json", "w") as json_file:
        json_str = json.dumps(dataContainer, indent=4)
        json_file.write(json_str)

        print("创建一个新文件： " + str(fileName))

def GetProptypeByIndex(index):
    if index == 0 or index == 1:
        return 1
    if index == 2 or index == 3:
        return 2
    if index == 4 or index == 5:
        return 3
    if index == 6 or index == 7:
        return 5
    if index == 8 or index == 9:
        return 6

wb = xw.Book("Club2Json.xlsx")
ws1 = wb.sheets['Sheet1']

column_index = 3
while ws1.range((2,column_index)).value != None:
    list_container = []
    for x in range(10):
        dic = {}
        club_id_row_index = x*2+2
        club_lv_row_index = x*2+3
        if ws1.range((club_id_row_index,column_index)).value != None:
            dic.update({"prop_id": int(ws1.range((club_id_row_index, column_index)).value)})
            dic.update({"prop_type": GetProptypeByIndex(x)})
            dic.update({"prop_num": 0})
            dic.update({"prop_level": int(ws1.range((club_lv_row_index, column_index)).value)})
            if x % 2 == 0:
                dic.update({"is_use": 1})
            else:
                dic.update({"is_use": 2})

        list_container.append(dic)

    Export2Json(str(ws1.range((1,column_index)).value), list_container)
    column_index += 1




