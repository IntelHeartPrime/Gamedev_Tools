
# 对结果进行排序处理
# 对所有的组合进行排序，取结果最大的前4个组合轮番写入新的Sheet之中

import xlwings as xw

wb = xw.Book("Props_config_Search.xlsx")
ws1 = wb.sheets['Search']
ws2 = wb.sheets['Order']

# 对结果进行排序
# 按照组合数量排序，取其index
# 按照第一杆数量排序，取其index
# 取前4个即可
# 组合数量 - 根据column的值反算出index
# 第一杆数量 - 根据column的值反算出index

''' 
补充 - 取最NB的组合就好  
'''

row_index = 3

while  ws1.range((row_index, 1)).value != None:

    print("")
    print(" ------------------ " + str(row_index) + " ------------------ ")

    list_result_index_store = []
    list_double_club_index_store = []
    list_single_club_index_store = []

    list_double_club = []
    list_double_club_sampleCnt = []

    list_single_club = []
    list_single_club_sampleCnt = []

    # double_club
    print("")
    print(" { double club 取值 } ")
    # 取值

    print("开始取值")

    for x in range(11):
        if ws1.range((row_index, x*8 + 11)).value != None:
            if int(ws1.range((row_index, x*8 +11)).value) >= 10:
                list_double_club.append(x)
                list_double_club_sampleCnt.append(ws1.range((row_index, x*8 + 11)).value)

    print("取值之后，list_double_club = " + str(list_double_club))
    print("取值之后，list_double_club_sampleCnt = " + str(list_double_club_sampleCnt))

    # 循环4次，取最大样本量所在的Index
    # 如果样本不够，则一定会取到重复的Index，去重即可

    if len(list_double_club) > 0:
        for x in range(4):
            max_value = max(list_double_club_sampleCnt)
            if (max_value != -1):
                for index in range(len(list_double_club)):
                    if list_double_club_sampleCnt[index] == max_value:
                        list_double_club_index_store.append(list_double_club[index])
                        list_double_club_sampleCnt[index] = -1
                        break

        print("循环4次后， list_double_club = " + str(list_double_club))
        print("循环4次后， list_double_club_sampleCnt = " + str(list_double_club_sampleCnt))
        print("循环4次后， list_double_club_index_store = " + str(list_double_club_index_store))

        # double_club 去重
        list_double_club_index_store = list(set(list_double_club_index_store))
        print("double_club 去重后 list_double_club_index_store = " + str(list_double_club_index_store))


    # 若double_club 不足四个，则 single_club取值
    if len(list_double_club_index_store) < 4:
        # 取值
        print("")
        print(" { single club 取值 } ")

        print("开始取值")
        for x in range(11):
            if ws1.range((row_index, x * 8 + 9)).value != None:
                if int(ws1.range((row_index, x*8 + 9)).value) > 10:
                    list_single_club.append(x)
                    list_single_club_sampleCnt.append(ws1.range((row_index, x * 8 + 9)).value)

        print("取值之后，list_single_club = " + str(list_single_club))
        print("取值之后，list_single_club_sampleCnt = " + str(list_single_club_sampleCnt))

        # 循环4次，取最大样本量所在的Index
        # 如果样本不够，则一定会取到重复的Index，去重即可
        if len(list_single_club) > 0:
            single_max_cnt = 4-len(list_double_club)
            for x in range(single_max_cnt):
                max_value = max(list_single_club_sampleCnt)
                if (max_value != -1) :
                    for index in range(len(list_single_club)):
                        if list_single_club_sampleCnt[index] == max_value:
                            list_single_club_index_store.append(list_single_club[index])
                            list_single_club_sampleCnt[index] = -1

            print("循环4次后， list_single_club = " + str(list_single_club))
            print("循环4次后， list_single_club_sampleCnt = " + str(list_single_club_sampleCnt))
            print("循环4次后， list_single_club_index_store = " + str(list_single_club_index_store))

            # single_club 去重
            list_single_club_index_store = list(set(list_single_club_index_store))
            print("single_club 去重后 list_single_club_index_store = " + str(list_single_club_index_store))


    # 综合处理
    print("")
    print(" [ 最后处理 ] ")

    list_result_index_store = list_double_club_index_store + list_single_club_index_store
    print("list_result_index_store = " + str(list_result_index_store))

    # list_result_index_store 去重
    list_result_index_store = list(set(list_result_index_store))
    print("list_result_index_store 去重后 list_result_index_store = " + str(list_result_index_store))

    ''' 去掉样本数量不足的组合 '''

    ''' 取样本数量最多的两个杆 并额外写入 '''

    # 取值

    #  { club_id: [club_level, club_sampleCnt]}
    club_1_maxCnt_dic = {}
    club_2_maxCnt_dic = {}

    print("")
    print(" {  样本数量最多的两个单杆取值 } ")

    # 列id 95-96； 97-98
    print(" start ")
    for x in range(11):
        if ws1.range((row_index, x * 8 + 9)).value != None:

            # 第一杆
            print("第一杆")
            club_id_1 = int(ws1.range((row_index, x*8 + 5)).value)
            club_level_1 = int(ws1.range((row_index,x*8 + 6)).value)
            club_sampleCnt_1 = int(ws1.range((row_index, x*8 + 9)).value)

            canFind = False
            for y in club_1_maxCnt_dic.keys():
                if str(club_id_1) == y:
                    print(club_sampleCnt_1)
                    list_rewrite = club_1_maxCnt_dic[y]
                    print(list_rewrite)
                    list_rewrite[0] = club_level_1
                    list_rewrite[1] = club_sampleCnt_1
                    print(" 重新赋值 - club_level_1 = " + str(club_level_1) + "  club_sampleCnt = " + str(club_sampleCnt_1))
                    canFind = True


            if(canFind == False):
                list_cache = [club_level_1, club_sampleCnt_1]
                club_1_maxCnt_dic.update({str(club_id_1): list_cache})
                print("添加值：" + str(club_id_1) + " list = " + str(list_cache))

        if ws1.range((row_index, x * 8 + 10)).value != None:

            # 避免第二杆无值的情况
            # 第二杆
            print("第二杆")
            club_id_2 = int(ws1.range((row_index, x*8 + 7)).value)
            club_level_2 = int(ws1.range((row_index,x*8 + 8)).value)
            club_sampleCnt_2 = int(ws1.range((row_index, x*8+ 10)).value)
            canFind = False
            for y in club_2_maxCnt_dic.keys():
                if str(club_id_2) == y:
                    list_rewrite = club_2_maxCnt_dic[y]
                    list_rewrite[0] = club_level_2
                    list_rewrite[1] = club_sampleCnt_2
                    print(" 重新赋值 - club_level_2 = " + str(club_level_2) + "  club_sampleCnt = " + str(club_sampleCnt_2))
                    canFind = True

            if(canFind == False):
                list_cache = [club_level_2, club_sampleCnt_2]
                club_2_maxCnt_dic.update({str(club_id_2): list_cache})
                print("添加值：" + str(club_id_2) + " list = " + str(list_cache))

    print("")
    print("dic_1 = " + str(club_1_maxCnt_dic))
    print("dic_2 = " + str(club_2_maxCnt_dic))
    # 取字典中最大值
    club_id_1_max = 0
    club_level_1_max = 0

    max_sample_cache = 0
    for z in club_1_maxCnt_dic.keys():
        list_get = club_1_maxCnt_dic[z]
        levelGet = list_get[0]
        sampleCnt = list_get[1]
        if sampleCnt >= max_sample_cache:
            club_id_1_max = int(z)
            club_level_1_max = levelGet
            max_sample_cache = sampleCnt

    club_id_2_max = 0
    club_level_2_max = 0

    max_sample_cache = 0
    for z in club_2_maxCnt_dic.keys():
        list_get = club_2_maxCnt_dic[z]
        levelGet = list_get[0]
        sampleCnt = list_get[1]
        if sampleCnt >= max_sample_cache:
            club_id_2_max = int(z)
            club_level_2_max = levelGet
            max_sample_cache = sampleCnt

    print("club_id_1_max = " + str(club_id_1_max) + " club_level_1_max = " + str(club_level_1_max))

    print("club_id_2_max = " + str(club_id_2_max) + " club_level_2_max = " + str(club_level_2_max))
    print("")


    ws2.range((row_index, 95)).value = club_id_1_max
    ws2.range((row_index, 96)).value = club_level_1_max
    ws2.range((row_index, 97)).value = club_id_2_max
    ws2.range((row_index, 98)).value = club_level_2_max

    ''' 根据result_index 将结果写入到 Order表中 '''



    # TODO 按照样本数量排序填入

    ws2.range((row_index, 1)).value = ws1.range((row_index, 1)).value
    ws2.range((row_index, 2)).value = ws1.range((row_index, 2)).value
    ws2.range((row_index, 3)).value = ws1.range((row_index, 3)).value

    for index in range(len(list_result_index_store)):
        # balls
        ws2.range((row_index, index*5 + 4)).value = ws1.range((row_index, list_result_index_store[index]*8 + 4)).value
        # clubs_id
        ws2.range((row_index, index*5 + 5)).value = ws1.range((row_index, list_result_index_store[index]*8 + 5)).value
        # clubs_level
        ws2.range((row_index, index*5 + 6)).value = ws1.range((row_index, list_result_index_store[index]*8 + 6)).value
        # clubs_id 2
        ws2.range((row_index, index*5 + 7)).value = ws1.range((row_index, list_result_index_store[index]*8 + 7)).value
        # clubs_level 2
        ws2.range((row_index, index*5 + 8)).value = ws1.range((row_index, list_result_index_store[index]*8 + 8)).value


    print (" write completed ")

    row_index += 1


# TODO 将所有的数据转秩处理
