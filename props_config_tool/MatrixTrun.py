'''
将数据表转秩成为特定格式
'''


import xlwings as xw

wb = xw.Book("Props_config_Search.xlsx")
ws1 = wb.sheets['Search']
ws2 = wb.sheets['Order']
ws3 = wb.sheets['Matrix']

# 95,96 ; 97,98
# read rows 95 ，creat a list

'''
row_index = 3
list_club_id_1 = []
list_club_level_1 = []

list_club_id_2 = []
list_club_level_2 = []

while ws2.range((row_index, 97)).value != None:
    if ws2.range((row_index, 97)).value != 0.0:
        canFind = False
        for x in list_club_id_1:
            if x == int(ws2.range((row_index, 97)).value):
                canFind = True
        if(canFind == False):
            list_club_id_1.append(int(ws2.range((row_index, 97)).value))

    row_index += 1

print(list_club_id_1)

start_column = 12
for x in list_club_id_1:
    ws3.range((2, start_column)).value = x
    start_column += 1

'''

# 生成矩阵对应list
# list_column_index , list_club_id

list_column_index = []
list_club_id = []

start_column = 4
while ws3.range((2, start_column)).value != None:
    list_column_index.append(int(ws3.range((1, start_column)).value))
    list_club_id.append(int(ws3.range((3, start_column)).value))

    start_column += 1

print(list_column_index)
print(list_club_id)

# 开始遍历

row_index = 4
while ws2.range((row_index, 1)).value != None:
    ws3.range((row_index, 1)).value = ws2.range((row_index, 1)).value
    ws3.range((row_index, 2)).value = ws2.range((row_index, 2)).value

    if ws2.range((row_index, 95)).value != None:

        # 第一杆
        club_id_get1 = int(ws2.range((row_index, 95)).value)
        club_level_get1 = int(ws2.range((row_index, 96)).value)

        for x in range(len(list_club_id)):
            if list_club_id[x] == club_id_get1:
                ws3.range((row_index, list_column_index[x])).value = club_level_get1
                print("")
                print(" 第一杆 ")
                print(" course_id = " + str(ws2.range((row_index, 2)).value) + " 杆id = " + str(club_id_get1) + \
                      " 等级 = " + str(club_level_get1))

    if ws2.range((row_index, 97)).value != None:

        # 第二杆
        club_id_get2 = int(ws2.range((row_index, 97)).value)
        club_level_get2 = int(ws2.range((row_index, 98)).value)

        for x in range(len(list_club_id)):
            if list_club_id[x] == club_id_get2:
                ws3.range((row_index, list_column_index[x])).value = club_level_get2
                print("")
                print(" 第二杆 ")
                print(" course_id = " + str(ws2.range((row_index, 2)).value) + " 杆id = " + str(club_id_get2) + \
                      " 等级 = " + str(club_level_get2))

    row_index += 1