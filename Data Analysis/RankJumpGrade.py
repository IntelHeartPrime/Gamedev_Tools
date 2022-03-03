
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

# 根据输入的开始值与结束值返回跳过的档位list
def get_jumped_ranks_by_start_end_points(start_points, end_points):

    start_rank, start_precent = get_rank_precent_byValue(start_points)
    end_rank, end_precent = get_rank_precent_byValue(end_points)

    jumped_rank = []
    if end_rank >= start_rank:
        




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
                print("origin_points = " + str(origin_points) + " end_points = " + str(end_points))
                # 判断本次跳过了哪些档位




