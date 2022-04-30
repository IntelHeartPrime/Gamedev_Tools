'''逐行解析csv，并把数据统计于Excel中'''
'''
先搜索csv，获取course_id
根据course_id搜索Excel，定位该场景的行数
如果course_id 不变，则对该行数区间内进行遍历，若单个杆或者组合符合，则对该杆进行+1 
" 如果csv中杆等级不足，亦然+1 "  --- 需设置一此开关 
" 若对于某一组合而言，csv中等级都低于其，则也对此组合+1 ，也需设置开关 " 
'''

'''
数据结构

缓存区 
不同杆的样本数量
例如：
[[id,level],[row_index, column_index],[cnt,0]] 
[id,level] 代表杆的id和等级
[row_index, column_index] 代表存储结果的位置的 row索引与column索引
[cnt,0] 代表应该填入的值

在更换course_id 后清零

组合
例如： [ [ a, b] , [ c, d] ,[final_value_row, final_value_column],[cnt,0]]  
[a,b] 代表第一杆的 club_id & club_level
[c,d] 代表第二杆的 club_id & club_level

[final_value_row, final_value_column] 代表存储其结果的位置的 row索引与column索引  - Excel中
[cnt,0] 代表应该填入的值 

是否需要唯一标识

'''

# 缓存
single_club_combination = []  # [[],[]..]
double_club_combination = []  # [[],[]..]

import csv
import xlwings as xw

# 读取csv并遍历

wb = xw.Book("Props_config_Search.xlsx")
ws1 = wb.sheets['Search']

csv_file_path = "clubDistributionSearch.csv"

with open(csv_file_path) as csvfile:

    f_csv = csv.reader(csvfile)

    index = 0

    last_course_id = 0
    now_course_id = 0

    start_cache = True

    for row in f_csv:
        if index >0:
            # 开始逻辑

            print("")
            print("-----------------------------------------")
            print(" 处理第 " + str(index) + " 条数据")
            '''   搜索球场 ,并定位search_row_index '''
            now_course_id = int(row[1])


            if now_course_id != last_course_id:

                # 在Clear之前进行数据的写入
                print("~~~~~~ data insert ~~~~~~")
                for unit in single_club_combination:
                    print(" * ")
                    row_1 = unit[1][0]
                    column_1 = unit[1][1]
                    result_1 = unit[2][0]
                    ws1.range((row_1, column_1)).value = result_1
                print(" single completed ")
                for unit in double_club_combination:
                    print(" ** ")
                    row_1 = unit[2][0]
                    column_1 = unit[2][1]
                    result_1 = unit[3][0]
                    ws1.range((row_1, column_1)).value = result_1

                print(" double completed ")


                # 重新search并定位
                search_row_index = 0
                print("")
                print(" ！！！ Clear Cache")
                single_club_combination.clear()
                double_club_combination.clear()
                print("")


                for x in range(3,152):
                    course_id_in_excel = int(ws1.range((x, 2)).value)
                    if now_course_id == course_id_in_excel:
                        search_row_index = x
                        print("「")
                        print(" 定位到该id的球场， row_index = " + str(search_row_index))
                        print("」")

                        start_cache = True

                        break

            else:
                # 如果now_course_id 相等，则不必再进行相应的 Store
                start_cache = False

            last_course_id = now_course_id

            '''     END     '''

            '''  对Excle 的单行进行解析， 并保存所有的Cache  '''
            if start_cache:
                # 单杆组合

                # search_row_index


                print(" 开始进行单杆组合的缓存 ")
                for x in range(11):
                    # 第一杆
                    if ws1.range((search_row_index, x*8+ 5)).value != None:

                        print(".")
                        unit_add = []
                        club_id = int(ws1.range((search_row_index, x*8 + 5)).value)
                        club_level = int(ws1.range((search_row_index, x*8 + 6)).value)
                        row_index_store = search_row_index
                        column_index_store = x*8 + 9

                        unit_add.append([club_id, club_level])
                        unit_add.append([row_index_store, column_index_store])
                        unit_add.append([0, 0])

                        single_club_combination.append(unit_add)

                    # 第二杆
                    if ws1.range((search_row_index, x * 8 + 7)).value != None:
                        print("..")
                        unit_add = []
                        club_id = int(ws1.range((search_row_index, x * 8 + 7)).value)
                        club_level = int(ws1.range((search_row_index, x * 8 + 8)).value)
                        row_index_store = search_row_index
                        column_index_store = x * 8 + 10

                        unit_add.append([club_id, club_level])
                        unit_add.append([row_index_store, column_index_store])
                        unit_add.append([0, 0])

                        single_club_combination.append(unit_add)


                print("该行内所有单杆组合缓存: ")
                for unit in single_club_combination:
                    print(unit)

                print("开始进行杆组合的缓存")

                # 第一杆&第二杆一起统计
                for x in range(11):
                    if (ws1.range((search_row_index, x * 8 + 5)).value != None) and (ws1.range((search_row_index, x * 8 + 7)).value != None):
                        print("...")
                        unit_add = []
                        club_id_1 = int(ws1.range((search_row_index, x*8 + 5)).value)
                        club_level_1 = int(ws1.range((search_row_index, x*8 + 6)).value)
                        club_id_2 = int(ws1.range((search_row_index, x * 8 + 7)).value)
                        club_level_2 = int(ws1.range((search_row_index, x * 8 + 8)).value)
                        row_index_store = search_row_index
                        column_index_store = x * 8 + 11

                        unit_add.append([club_id_1, club_level_1])
                        unit_add.append([club_id_2, club_level_2])
                        unit_add.append([row_index_store, column_index_store])
                        unit_add.append([0, 0])

                        double_club_combination.append(unit_add)

                print("该行内所有双杆组合缓存： ")
                for unit in double_club_combination:
                    print(unit)

            '''     END     '''

            ''' 对单行数据进行解析，遍历缓存进行数据量统计 '''

            club_id_1 = int(row[2])
            club_level_1 = int(row[3])

            club_id_2 = int(row[4])
            club_level_2 = int(row[5])

            sample_cnt = int(row[6])

            # single 的遍历
            print ("单杆数据检验")
            for single_unit in single_club_combination:
                print(single_unit)

                print("club_id_1: " + str(club_id_1) + " - club_level_1: " + str(club_level_1) + " vs " + str(single_unit))
                if club_id_1 == single_unit[0][0]:
                    if club_level_1 <= single_unit[0][1]:
                        single_unit[2][0] = single_unit[2][0] + sample_cnt
                        print("符合样本 + " + str(sample_cnt))

                print("club_id_2: " + str(club_id_2) + " - club_level_2 " + str(club_level_2) + " vs " + str(single_unit))
                if club_id_2 == single_unit[0][0]:
                    if club_level_2 <= single_unit[0][1]:
                        single_unit[2][0] = single_unit[2][0] + sample_cnt
                        print("符合样本 + " + str(sample_cnt))

            # double club 的遍历
            print("")
            print ("双杆数据检验")
            for double_unit in double_club_combination:
                print("{")
                print("club_id_1: " + str(club_id_1) + " - club_level_1: " + str(club_level_1))
                print("club_id_2: " + str(club_id_2) + " - club_level_2: " + str(club_level_2))
                print("vs")
                print(str(double_unit))
                print("}")

                if club_id_1 == double_unit[0][0]:
                    if club_level_1 <= double_unit[0][1]:
                        if club_id_2 == double_unit[1][0]:
                            if club_level_2 <= double_unit[1][1]:
                                double_unit[3][0] = double_unit[3][0] + sample_cnt
                                print("符合样本 + " + str(sample_cnt))


            print("")
            print("completed check")
            print("「 ------")
            print("result = ")
            print("single:")
            for x in single_club_combination:
                print(x)
            print("double:")
            for x in double_club_combination:
                print(x)

            print("------ 」")

            '''     END     '''


            ''' 遍历缓存区，进行结果输出 '''


            '''     END     '''




        start_cache = False
        index += 1






