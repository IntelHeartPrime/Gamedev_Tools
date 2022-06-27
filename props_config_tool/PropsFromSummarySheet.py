# 如何处理
# 遍历一层 - 标的列，获取标的列column 2~100
# 定位杆 - 根据第一行找值，有值者列存入list -{ 具体杆的lv}
# 函数 - 得出此行第一杆 元组[(id,lv),(id,lv)] &第二杆
# 生成Props
# 对sheet s5~s19分别做此

'''
输出格式；
"props": "[{\"balls\":[1],\"clubs\":[{\"id\":19,\"level\":5,\"w\":0.5},{\"id\":26,\"level\":2,\"w\":0.5}]}]",

x0 x1
[{"id":37,"l":4,"r":5},{"id":38,"l":4,"r":5}]
'''

# 下载文件

import requests
import xlwings as xw
import os
import json

url_download = 'https://docs.google.com/spreadsheets/d/1KJAA-M-noxzXAQ3W5Vt0an_zELwsDiXL88iVAt49fFI/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('MultipleStartPos.xlsx', 'wb').write(xlsx_file.content)

wb = xw.Book("MultipleStartPos.xlsx")

json_file_name = "props_new"

list_all = []
dic_x0x1 = {}

class Club_prop:
    def __init__(self):
        self.club_id = 0
        self.club_lv = 0
        self.club_type = 0

    def printInfo(self):
        print("Club_prop club_id = " +str(self.club_id) + " club_lv = " + \
              str(self.club_lv) + " club_type = " + str(self.club_type))

class Club_unit:
    def __init__(self, club_id):
        self.club_type = 0
        self.club_id = club_id
        self.getTypeById()
        self.club_location = 0  #第一杆还是第二杆？根据整体情况综合决定
        self.column_index = 0

    def getTypeById(self):
        # type = 1  Driver
        # type = 2  wood
        # type = 3  Iron
        # type = 5  Wedge
        # type = 6  SandWedge
        type1_list = [19, 31, 37, 64]
        type2_list = [26, 32, 38, 63]
        type3_list = [27, 39, 45]
        type6_list = [60]

        for value in type1_list:
            if value == self.club_id:
                self.club_type = 1
                print("club_id = " + str(self.club_id) + "  club_type = " + str(self.club_type))
                return None
        for value in type2_list:
            if value == self.club_id:
                self.club_type = 2
                print("club_id = " + str(self.club_id) + "  club_type = " + str(self.club_type))
                return None
        for value in type3_list:
            if value == self.club_id:
                self.club_type = 3
                print("club_id = " + str(self.club_id) + "  club_type = " + str(self.club_type))
                return None
        for value in type6_list:
            if value == self.club_id:
                self.club_type = 6
                print("club_id = " + str(self.club_id) + "  club_type = " + str(self.club_type))
                return None
        print("nothing!!!")
        raise ValueError

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value

# 传入几个list，判断其count>0 的list数量
def howMuchListCountRaise0(list_all):
    result = 0
    for list_in in list_all:
        if len(list_in)>0:
            result += 1
    print("result = " + str(result))
    return result


# 函数 - 输入（行数），输出某行第一杆与第二杆
def GetFirstClubsAndSecondClubs( row_index ):
    '''
    :param row_index: 行索引
    :return: [list,..]
    # 脚本转写非常重要
    # 周末多打几把游戏
    
    '''

    return None


# 函数 - 开始转sheetX的配置
def ExchangeConfig( sheet_name, tour_id ):
    '''
    :param sheet_name: 表名称
    :param tour_id: tour_id
    :return:
    '''

    print("------ 开始转换" + str(sheet_name) + " --------")
    ws1 = wb.sheets[sheet_name]
    # 定位"第一杆权重？" 与 "第二杆权重？"列索引
    first_club_weight_column = 0
    second_club_weight_column = 0

    for y in range(1,100):
        if ws1.range((2,y)).value == "第一杆权重？":
            first_club_weight_column = y
        if ws1.range((2,y)).value == "第二杆权重？":
            second_club_weight_column = y
    print("第一杆权重列索引 = " + str(first_club_weight_column))
    print("第二杆权重列索引 = " + str(second_club_weight_column))

    # 进行第一行的转写
    club_unit_list = []    # x0 x1 主要使用的对象
    column_index = 1
    while ws1.range((1, column_index)).value != "标的":
        if ws1.range((1, column_index)).value != None:
            if ws1.range((1, column_index)).value != "标的":
                print("column_index = " + str(column_index))
                club_id_1 = int(ws1.range((1, column_index)).value)
                print("club_id = " + str(club_id_1))
                club_unit1 = Club_unit(club_id_1)
                club_unit1.column_index = column_index
                club_unit_list.append(club_unit1)
        column_index += 1

    # 找到标的的那行
    biaodi_column_index = 0
    for x in range(1,50):
        if str(ws1.range((1, x)).value) == "标的":
            biaodi_column_index = x
    print("标的列坐标 = " + str(biaodi_column_index))

    # 逐行进行处理
    for row in range(3, 50):
        print(" 开始 ，处理第 " + str(row) + " 行数据")
        if ws1.range((row, biaodi_column_index)).value != None:

            course_id = int(ws1.range((row, biaodi_column_index)).value)
            print("course_id = " + str(course_id))

            ''' 普通场 or 决胜场'''
            course_type = 0  # 1是普通场，2是决胜场
            first_club_weight = 0.0  # 第一杆权重
            second_club_weight = 0.0  # 第二杆权重

            # 先判断是普通场还是决胜场
            if ws1.range((row, first_club_weight_column)).value != None and ws1.range(
                    (row, second_club_weight_column)).value != None:
                course_type = 1
                first_club_weight = ws1.range((row, first_club_weight_column)).value
                second_club_weight = ws1.range((row, second_club_weight_column)).value
                print("普通场")
                print("第一杆权重 = " + str(first_club_weight))
                print("第二杆权重 = " + str(second_club_weight))

            if ws1.range((row, first_club_weight_column)).value != None and ws1.range(
                    (row, second_club_weight_column)).value == None:
                course_type = 2
                print("决胜场")
                first_club_weight = ws1.range((row, first_club_weight_column)).value
                print("第一杆权重 = " + str(first_club_weight))

            print(" course_type = " + str(course_type))

            ''' 其他处理 '''

            club_prop_list = []
            club_prop_first = []  # 第一杆
            club_prop_second = []  # 第二杆

            for unit in club_unit_list:
                if ws1.range((row, unit.column_index)).value != None:
                    club_obj = Club_prop()
                    club_obj.club_id = unit.club_id
                    club_obj.club_lv = int(ws1.range((row, unit.column_index)).value)
                    club_obj.club_type = unit.club_type
                    club_prop_list.append(club_obj)

            # 对第一杆与第二杆进行判定
            print(" ----- 开始props 的判定了 -------" + str(row) + " -- 行 ")
            # 对所有type进行归类处理
            club_prop_type1 = []
            club_prop_type2 = []
            club_prop_type3 = []
            club_prop_type5 = []
            club_prop_type6 = []

            for prop in club_prop_list:
                if prop.club_type == 1:
                    club_prop_type1.append(prop)
                if prop.club_type == 2:
                    club_prop_type2.append(prop)
                if prop.club_type == 3:
                    club_prop_type3.append(prop)
                if prop.club_type == 5:
                    club_prop_type5.append(prop)
                if prop.club_type == 6:
                    club_prop_type6.append(prop)

            # 如果有三个以上类型杆的count>0 则报错
            if howMuchListCountRaise0([club_prop_type1, club_prop_type2, club_prop_type3, club_prop_type5, club_prop_type6]) >= 3:
                print("怎么有三个以上的类型的杆？")
                raise ValueError

            # 如果没有一个杆，则报错
            if howMuchListCountRaise0([club_prop_type1, club_prop_type2, club_prop_type3, club_prop_type5, club_prop_type6]) == 0:
                print("没有一种类型的杆？")
                raise ValueError

            # 如果只有一类杆，则只添加第一杆 Speicial
            if howMuchListCountRaise0(
                    [club_prop_type1, club_prop_type2, club_prop_type3, club_prop_type5, club_prop_type6]) == 1:
                # 如果只有type2的个数>1且为普通场，其他为0则说明只有一个杆
                print("开始处理 - 只有1类杆")
                if len(club_prop_type2) > 0 and len(club_prop_type1) == 0 and len(club_prop_type3) == 0 and \
                        len(club_prop_type5) == 0 and len(club_prop_type6) == 0 and course_type == 1:
                    for club in club_prop_type2:
                        print("第一杆 & 第二杆都处理")
                        club_prop_first.append(club)
                        club_prop_second.append(club)
                else:
                    # 只有一类杆
                    print("只有一杆")
                    if len(club_prop_type1) > 0:
                        print("type1 为first ")
                        for club in club_prop_type1:
                            club_prop_first.append(club)
                    if len(club_prop_type2) > 0:
                        print("type2 为first ")
                        for club in club_prop_type2:
                            club_prop_first.append(club)
                    if len(club_prop_type3) > 0:
                        print("type3 为first ")
                        for club in club_prop_type3:
                            club_prop_first.append(club)
                    if len(club_prop_type5) > 0:
                        print("type5 为first ")
                        for club in club_prop_type5:
                            club_prop_first.append(club)
                    if len(club_prop_type6) > 0:
                        print("type6 为first ")
                        for club in club_prop_type6:
                            club_prop_first.append(club)

            # 有两类杆，则正常处理
            if len(club_prop_type2) >0 and ( len(club_prop_type1) > 0 or len(club_prop_type3) > 0 or \
                                             len(club_prop_type5) >0 or len(club_prop_type6) > 0):
                if len(club_prop_type1) > 0:
                    print("type1 为first ")
                    for club in club_prop_type1:
                        club_prop_first.append(club)
                    for club in club_prop_type2:
                        club_prop_second.append(club)
                if len(club_prop_type3) > 0:
                    print("type3 为first ")
                    for club in club_prop_type3:
                        club_prop_first.append(club)
                    for club in club_prop_type2:
                        club_prop_second.append(club)
                if len(club_prop_type5) > 0:
                    print("type5 为first ")
                    for club in club_prop_type5:
                        club_prop_first.append(club)
                    for club in club_prop_type2:
                        club_prop_second.append(club)
                if len(club_prop_type5) > 0:
                    print("type6 为first ")
                    for club in club_prop_type5:
                        club_prop_first.append(club)
                    for club in club_prop_type2:
                        club_prop_second.append(club)



            # 处理完成，使用组合方式输出props
            # balls为空，需要添加权重
            # 权重
            # 如何区分普通场与决胜场，权重只填了一个则为决胜场

            dic_course = {}
            list_all.append(dic_course)

            dic_course.update({"tour": tour_id})
            dic_course.update({"course_id": course_id})
            dic_course.update({"id": course_id})

            props_list = []
            dic_course.update({"props": props_list})

            if len(club_prop_first)>0 and len(club_prop_second)>0:
                for club1 in club_prop_first:
                    for club2 in club_prop_second:
                        dic_prop = {}
                        props_list.append(dic_prop)
                        dic_prop.update({"balls": []})
                        clubs = []
                        dic_prop.update({"clubs": clubs})

                        # club1
                        club1_dic = {}
                        clubs.append(club1_dic)
                        club1_dic.update({"id": club1.club_id})
                        club1_dic.update({"level": club1.club_lv})
                        club1_dic.update({"w": first_club_weight})

                        # club2
                        club2_dic = {}
                        clubs.append(club2_dic)
                        club2_dic.update({"id": club2.club_id})
                        club2_dic.update({"level": club2.club_lv})
                        club2_dic.update({"w": second_club_weight})
            if len(club_prop_first)>0 and len(club_prop_second)==0:
                for club1 in club_prop_first:
                    dic_prop = {}
                    props_list.append(dic_prop)
                    dic_prop.update({"balls": []})
                    clubs = []
                    dic_prop.update({"clubs": clubs})

                    # club1
                    club1_dic = {}
                    clubs.append(club1_dic)
                    club1_dic.update({"id": club1.club_id})
                    club1_dic.update({"level": club1.club_lv})
                    club1_dic.update({"w": first_club_weight})

    ''' x0x1 的转换 '''
    # 取 x0,x1 所在的行坐标

    row_x0 = 0
    row_x1 = 0
    for y in range(1,50):
        if ws1.range((y,1)).value == "x0":
            row_x0 = y
        if ws1.range((y,1)).value == "x1":
            row_x1 = y

    list_x0x1 = []
    for club in club_unit_list:
        if ws1.range((row_x0, club.column_index)).value != None:
            dic ={}
            dic.update({"id": club.club_id})
            dic.update({"l": int(ws1.range((row_x0, club.column_index)).value)})
            dic.update({"r": int(ws1.range((row_x1, club.column_index)).value)})

            list_x0x1.append(dic)

    dic_x0x1.update({str(tour_id): list_x0x1})




sheet_names = ["s5","s6","s7","s8","s9","s10","s11","s12","s13",\
               "s14","s15","s16","s17","s18","s19"]

tour_ids = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

test_sheet_names = ["s5","s6"]
test_tour_ids = [5,6]

index = 0
for sheet in sheet_names:
    ExchangeConfig(sheet, tour_ids[index])
    index += 1


def Export2Json(fileName, dataContainer):
    with open(fileName+".json", "w") as json_file:
        json_str = json.dumps(dataContainer, indent=4)
        json_file.write(json_str)

        print("创建一个新文件： " + str(fileName))

Export2Json(json_file_name, list_all)
Export2Json("x0x1", dic_x0x1)

