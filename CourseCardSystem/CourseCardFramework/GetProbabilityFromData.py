# 读取Csv文件，从而得出各个区间下的权重

import xlwings as xw
import csv

wb = xw.Book("CourseCardsSystem.xlsx")
ws = wb.sheets['Sheet1']

# Birde
birde_file_name = "Birde_data.csv"
birde_column_index = 16
birde_column_output_index = 18

# Eagle
eagle_file_name = "Eagle_data.csv"
eagle_column_index = 20
eagle_column_output_index = 22

# Albatross
albatross_file_name = "Albatross_data.csv"
albatross_column_index = 24
albatross_column_output_index = 26

# 读取数据并且输出到特定表格下的函数
def getProbabilityFromData(file_name, column_index, column_output_index):
    '''
    :param file_name: 要读取的csv文件名称
    :param column_index: 要读取的距离范围的数据列
    :param column_output_index: 要输出的区间权重的数据列
    :return: 输出到权重区间表格内就好
    '''

    # 逐行遍历 csv
    # 当其处于特定区间内时，特定区间 Value+1
    # 最后输出为特定区间的权重

    # 读取距离数据
    distance_list = []
    csv_file_path = file_name
    with open(csv_file_path) as csvfile:
        f_csv = csv.reader(csvfile)
        index = 0
        for row in f_csv:
            if index>0:
                dis_cache = float(row[0])
                distance_list.append(dis_cache)
            index =  index + 1

    # 生成区间数据
    section_data = []

    row_index = 4
    while ws.range((row_index, column_index)).value != None:
        section_data.append(ws.range((row_index, column_index)).value)
        row_index = row_index + 1
    print("区间值 = ")
    print(section_data)
    section_data_cnt = []

    for x in section_data:
        section_data_cnt.append(0)

    # 开始计数
    ''' 此算法要求 Excel中距离区间必然按照从大到小排序 '''

    single_grade_cnt = 0

    for dis in distance_list:
        index = -1
        for section in section_data:
            if dis<=section:
                index = index+1
        print( "dis = " + str(dis) + " 其index= " + str(index) )
        if index == -1:
            single_grade_cnt = single_grade_cnt + 1
        else:
            section_data_cnt[index] = section_data_cnt[index] + 1

    # 输出最后的权重
    print("不再距离之内权重 = " + str(single_grade_cnt))
    print("权重List =" )
    print(section_data_cnt)

    # 打印到Excel中
    ws.range((3,column_output_index)).value = single_grade_cnt
    row_index = 4
    for x in section_data_cnt:
        ws.range((row_index, column_output_index)).value = x
        row_index = row_index + 1


# Birde 权重
getProbabilityFromData(birde_file_name, birde_column_index,birde_column_output_index)

# Eagle 权重
getProbabilityFromData(eagle_file_name, eagle_column_index,eagle_column_output_index)

# Albatross 权重
getProbabilityFromData(albatross_file_name, albatross_column_index,albatross_column_output_index)



