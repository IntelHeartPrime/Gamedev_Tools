import os
import csv

csv_file_path = "paid_data_groupBy.csv"





# 分析tag，对其进行拆分，从而统计出其总点数获得
# 进而计算出按照目前的档位分配其处于何种档位，何种进度

progress_points = [0,80,170,270,360,480,630,750,930,1180,1360,1620,1960,2220,2600,3100,3480,4020,4720,5260,6010,6960]
# >=0 & < 80 now = 0 next = 1


free = 10
token = 60
gift1 = 100
gift2 = 170
gift3 = 300
gift4 = 650
gift5 = 1100

sum_points_list = []
tag_list = []
cnt_list = []
rank_list = []
precent_list =[]


with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)

    index = 0
    for row in f_csv:
        # read csv successful
        if index > 0:
            mode_str = row[0]
            cnt = row[1]

            tag_list.append(mode_str)
            cnt_list.append(cnt)

            mode_str_list = mode_str.split('-')

            sum_points = 0
            for x in mode_str_list:
                if x == "free":
                    sum_points= sum_points + free
                if x == "token":
                    sum_points= sum_points + token
                if x == "gift1":
                    sum_points= sum_points + gift1
                if x == "gift2":
                    sum_points= sum_points + gift2
                if x == "gift3":
                    sum_points= sum_points + gift3
                if x == "gift4":
                    sum_points= sum_points + gift4
                if x == "gift5":
                    sum_points= sum_points + gift5
            sum_points_list.append(sum_points)
        index = index + 1

# 根据输入的值输出rank与precent
def get_rank_precent_byValue( input_value ):
    rank = 0
    precent = 0.0
    for x in range(len(progress_points)):
        if x < (len(progress_points) - 1) :
            if input_value >= progress_points[x] and input_value < progress_points[x+1]:
                #print("input_value = " + str(input_value) + " left_value = " + str(progress_points[x]) +\
                            #" right_value = " + str(progress_points[x+1]))
                rank = x
                precent = (input_value - progress_points[x])/ (progress_points[x+1] - progress_points[x])
        else:
            if input_value >= progress_points[x]:
                rank = x
                precent = 100.0

    return rank,precent



# 根据 sum_points_list 计算进度
for x in range(len(sum_points_list)):
    rank,precent = get_rank_precent_byValue(sum_points_list[x])
    rank_list.append(rank)
    precent_list.append(precent)



for x in range(len(tag_list)):
    tag_str = tag_list[x]
    cnt_str = cnt_list[x]
    sum_str = sum_points_list[x]
    rank_str = rank_list[x]
    precent_str = precent_list[x]

    print(str(tag_str) + " - " + str(cnt_str) + " - " + str(sum_str) + " - " + str(rank_str) +\
          " - " + str( precent_str))


# 计算 progress bar中进度条50%以上占比
than_50_cnt = 0

for x in precent_list:
    if x >= 0.5:
        than_50_cnt = than_50_cnt + 1

print(than_50_cnt / (len(precent_list)))

# 输出 有多人人达到这一层
rank_store_info = []
for y in range(len(progress_points)):
    rank_store_info.append(0)

for x in range(len(rank_list)):
    for y in range(len(rank_store_info)):
        if rank_list[x] == y:
            rank_store_info[y] = rank_store_info[y] + int(cnt_list[x])

for x in rank_store_info:
    print(x)


