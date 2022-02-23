# 读取Csv文件，从而得出各个区间下的权重

import xlwings

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
    :return:
    '''

    # 逐行遍历 csv
    # 当其处于特定区间内时，特定区间 Value+1
    # 最后输出为特定区间的权重
