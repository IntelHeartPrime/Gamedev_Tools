import os
import csv

csv_file_path = "data.csv"

# 分析tag，对其进行拆分，从而统计出其总点数获得
# 进而计算出按照目前的档位分配其处于何种档位，何种进度


free = 10
token = 60
gift1 = 100
gift2 = 170
gift3 = 300
gift4 = 650
gift5 = 1100

with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)

    index = 0
    for row in f_csv:
        # read csv successful
        if index > 0:
            mode_str = row[0]
            mode_str_list = mode_str.split('-')
