import json
import csv

# 读取csv
# 将csv输出为json

# Csv配置格式 level, min, max, grade, prop_type, prop_id, prop_num, prop_color, chest_type
# 读取Csv后按照逐行写进Json中

import os
work_dir = os.getcwd()
csv_file_path = "data.csv"

csv_dir = os.path.join(work_dir, csv_file_path)
print(csv_dir)

ticket_list = [0,80,170,270,360,480,630,750,930,1180,1360,1620,1960,2220,2600,3100,3480,4020,4720,5260,6010,6960]
dic_result = {}
dic_remark = {}
dic_rate = {}

for x in range(22):
    dic_result.update({str(x): 0})
    dic_remark.update({str(x): 0})
    dic_rate.update({str(x): 0.0})


def GetRankByTicket( ticket ):
    index = 0
    for x in ticket_list:
        if (index < len(ticket_list)-1):
            if ticket_list[index] <= ticket < ticket_list[index + 1]:
                return index+1
        else:
            if ticket_list[index] <= ticket:
                return index
        index = index + 1
    return 0

with open(csv_dir) as f:
    f_csv = csv.reader(f)
    row_index = 0
    for row in f_csv:
        if row_index != 0:
            last_value = int(row[3])
            now_value = last_value + int(row[2])

            last_rank = GetRankByTicket(last_value)
            now_rank = GetRankByTicket(now_value)

            value_cache_1 = dic_remark[str(now_rank)]
            dic_remark[str(now_rank)] = value_cache_1 + 1

            if now_rank-last_rank>=1:
                index = 0
                for x in range(now_rank - last_rank):
                    if index != 0:
                        value_cache = dic_result[str(last_rank+index)]
                        dic_result[str(last_rank+index)] = value_cache + 1
                    index = index + 1
        row_index = row_index + 1

print (dic_result)
print( dic_remark)

for x in dic_remark.keys():
    if( dic_remark[x]!= 0):
        dic_rate[x] =  float(dic_result[x]) / float(dic_remark[x])

print(dic_rate)

print(" ---- ")
for x in dic_rate.values():
    print(x)
