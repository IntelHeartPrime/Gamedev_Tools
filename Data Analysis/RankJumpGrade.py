
# 计算哪里档位被跳过了
# 当档位被经历时 value + 1
# 当档位被跳过时 value - 1
# 根据每个玩家的单笔付费进行计算
progress_points = [0,80,170,270,360,480,630,750,930,1180,1360,1620,1960,2220,2600,3100,3480,4020,4720,5260,6010,6960]
# >=0 & < 80 now = 0 next = 1

jump_times = []
for x in progress_points:
    jump_times.append(0)

free = 10
token = 60
gift1 = 100
gift2 = 170
gift3 = 300
gift4 = 650
gift5 = 1100

import csv

csv_file_path = "output_data_paid_player.csv"

with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)

    index = 0
    for row in f_csv:
        # read csv successful
        if index > 0:
            mode_str = row[2]
            mode_str_list = mode_str.split('-')
            



