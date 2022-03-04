
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

# 每次购买之前所看到的那个奖励为显示+1
def get_viewed_ranks_by_start_points(start_points):
    start_rank, start_precent = get_rank_precent_byValue(start_points)
    if start_rank< len(progress_points) - 1:
        start_rank = start_rank + 1
        # 这就是被跳过的档位
    return start_rank




# 根据输入的开始值与结束值返回跳过的档位list
def get_jumped_ranks_by_start_end_points(start_points, end_points):

    start_rank, start_precent = get_rank_precent_byValue(start_points)
    end_rank, end_precent = get_rank_precent_byValue(end_points)

    start_rank_float = float(start_rank) + start_precent
    end_rank_float = float(end_rank) + end_precent

    # 静止状态下能看到的不算跳过
    start_rank_float = start_rank_float + 1.0
    print(" start_rank_float = " + str(start_rank_float) + " end_rank_float = " + str(end_rank_float))
    jumped_rank = []
    if end_rank_float >= start_rank_float:

        # 求两者之间的整数
        # 即为跳过的档位

        for y in range(len(progress_points)):
            if float(y) > start_rank_float and float(y) <= end_rank_float:
                # 则 y档是跳过档
                jumped_rank.append(y)

    print("跳过档位" + str(jumped_rank))
    return jumped_rank

print(get_jumped_ranks_by_start_end_points(100,1000))


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

            sum_points = 0
            for x in mode_str_list:

                origin_points = sum_points

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

                end_points = sum_points
                # print("origin_points = " + str(origin_points) + " end_points = " + str(end_points))
                # 判断本次跳过了哪些档位
                jumped_list_cache = get_jumped_ranks_by_start_end_points(origin_points, end_points)

                # 看有多少档位被看到？？？
                viewed_rank = get_viewed_ranks_by_start_points(origin_points)

                # 对本次跳过进行统计
                for value in jumped_list_cache:
                    jump_times[value] = jump_times[value] + 1

                jump_times[viewed_rank] = jump_times[viewed_rank] - 1


        index = index + 1

# 输出最后结果
for x in jump_times:
    print(x)




