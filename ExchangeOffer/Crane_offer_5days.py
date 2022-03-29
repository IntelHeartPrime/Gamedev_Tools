# 逻辑
# 数据初值为：rank_count 档位数, ranks [] 各个档位所需要的累计Ticket值
# 数据输入列：[index, Free,Token,Gift1,Gift2,Gift3,Gift4,Gift5]
# 数据输出列：[index, sum_tickets, consume_dollar, now_rank, next_rank, percent, if_more_than_50, buy_5or10_upgrade, buy_5or10or20_upgrade]
# 构造函数，标记所有经典列
# 构造函数，输入列后导出输出列
# 构造函数，汇总所有结果
# 汇总的数据为：
# 所有经典组合买小额礼包可进档位占比， 所有经典组合买中中小额礼包可进档位占比，经典组合中进度条>50%占比
# 所有组合买小额礼包可进档位占比， 所有组合买中中小额礼包可进档位占比，所有组合中进度条>50%占比
# 花费前1/3的人所有组合买小额礼包可进档位占比， 花费前1/3的人所有组合买中中小额礼包可进档位占比，所有组合中进度条>50%占比

# 进阶 - 粗略自动化调参 -> 机器学习
# 主要调节各个档位的rank值，要求如下约束：1.是10的整数 2.数值逐渐变大 3.想加之和=最大积分Ticket量
# 构造方式进行自动化调参，遍历更多情况，要求以上指标取得最佳效果

# 初值

import csv

free_dollar = 0
token_dollar = 0
gift1_dollar = 4.99
gift2_dollar = 9.99
gift3_dollar = 19.99
gift4_dollar = 49.99
gift5_dollar = 99.99

free_ticket = 10
token_ticket = 60
gift1_ticket = 100
gift2_ticket = 170
gift3_ticket = 300
gift4_ticket = 650
gift5_ticket = 1100

ranks = [90,210,360,520,690,870,1060,1260,1470,1690,1920,2160,2420,2700,3000,3330,3690,4080,4500,4960,5460,6000,6580,7200,7870,8590,9360,10180,11040,11950]
rank_count = len(ranks)

# 输入列s
input_lists = []  # 2d list

# 输出列
output_lists = []  # 2d list


# 传入输入列后，返回输出列
def output_result_list(input_unit):
    # 填充index
    index = input_unit[0]

    # 计算sum_tickets
    sum_tickets = input_unit[1] * free_ticket + input_unit[2] * token_ticket + input_unit[3] * gift1_ticket + \
                  input_unit[4] \
                  * gift2_ticket + input_unit[5] * gift3_ticket + input_unit[6] * gift4_ticket + input_unit[
                      7] * gift5_ticket

    # 计算 consume_dollar
    consume_dollar = input_unit[1] * free_dollar + input_unit[2] * token_dollar + input_unit[3] * gift1_dollar + \
                     input_unit[4] \
                     * gift2_dollar + input_unit[5] * gift3_dollar + input_unit[6] * gift4_dollar + input_unit[
                         7] * gift5_dollar

    # 计算 now_rank 与 next_rank 与 percent

    now_rank = 0.0
    next_rank = 0.0
    percent = 0.0

    # 求 now_rank ，next_rank, percent，if_more_than_50
    result_unit = get_rank_percent(sum_tickets)
    now_rank = result_unit[0]
    next_rank = result_unit[1]
    percent = result_unit[2]
    if_more_than_50 = result_unit[3]

    # 计算buy_5or10_upgrade

    buy_5or10_upgrade = 0.0
    if input_unit[3] < 5:
        # 判断是否再买1个新的Gift1就可以晋级？
        now_rank_new = get_rank_percent(sum_tickets + gift1_ticket)[0]
        if now_rank_new > now_rank:
            buy_5or10_upgrade = 1.0
        else:
            if input_unit[4] < 5:
                # 判断是否再买1个新的Gift2就可以晋级？
                now_rank_new = get_rank_percent(sum_tickets + gift2_ticket)[0]
                if now_rank_new > now_rank:
                    buy_5or10_upgrade = 1.0

    # 计算buy_5or10or20_upgrade
    buy_5or10or20_upgrade = 0.0

    if buy_5or10_upgrade == 1.0:
        buy_5or10or20_upgrade = 1.0
    else:
        if input_unit[5] < 5:
            # 判断是否再买1个新的Gift3就可以晋级？
            now_rank_new = get_rank_percent(sum_tickets + gift3_ticket)[0]
            if now_rank_new > now_rank:
                buy_5or10or20_upgrade = 1.0

    output_unit = [index, sum_tickets, consume_dollar, now_rank, next_rank, percent, if_more_than_50, buy_5or10_upgrade,
                   buy_5or10or20_upgrade]
    return output_unit


# 把求 now_rank ，next_rank, percent,if_more_than_50 包装为一个函数
def get_rank_percent(sum_tickets):
    now_rank = 0.0
    next_rank = 0.0
    percent = 0.0

    if sum_tickets >= ranks[len(ranks) - 1]:
        now_rank = len(ranks)
        next_rank = len(ranks)
        percent = 1.0
    else:
        for x in range(len(ranks)):
            if sum_tickets <= ranks[x]:
                now_rank = x
                next_rank = x + 1
                if x != 0:
                    percent = (sum_tickets - ranks[x - 1]) / (ranks[x] - ranks[x - 1])
                else:
                    percent = sum_tickets / ranks[x]
                break

    if percent >= 0.5:
        if_more_than_50 = 1.0
    else:
        if_more_than_50 = 0.0

    result = [now_rank, next_rank, percent, if_more_than_50]
    return result


# 按照模式生成所有的组合
# 把所有的组合按照某一模式进行运算
# 输出为csv


Free = [5]
Token = [0, 1, 2, 3, 4, 5]
Gift1 = [0, 1, 2, 3, 4, 5]
Gift2 = [0, 1, 2, 3, 4, 5]
Gift3 = [0, 1, 2, 3, 4, 5]
Gift4 = [0, 1, 2, 3, 4, 5]
Gift5 = [0, 1, 2, 3, 4, 5]

index = 0

# 按照模式生成所有的组合

for free_unit in Free:
    for Token_unit in Token:
        for Gift5_unit in Gift5:
            for Gift4_unit in Gift4:
                for Gift3_unit in Gift3:
                    for Gift2_unit in Gift2:
                        for Gift1_unit in Gift1:
                            index = index + 1
                            result_unit = [index, free_unit, Token_unit, Gift1_unit, Gift2_unit, Gift3_unit,
                                           Gift4_unit, Gift5_unit]
                            input_lists.append(result_unit)

# 把所有的组合按照某一模式进行运算
for x in input_lists:
    output_unit = output_result_list(x)
    output_lists.append(output_unit)

sum_5or10_upgrade = 0
sum_5or10or20_upgrade = 0
sum_morethan50 = 0

# 输出总报告
for x in output_lists:
    # print(x)

    # 汇总的数据为：
    # 所有组合买小额礼包可进档位占比， 所有组合买中小额礼包可进档位占比，所有组合中进度条>50%占比
    # 花费前1/3的人所有组合买小额礼包可进档位占比， 花费前1/3的人所有组合买中中小额礼包可进档位占比，所有组合中进度条>50%占比
    # 数据输出列：[index, sum_tickets, consume_dollar, now_rank, next_rank, percent, if_more_than_50, buy_5or10_upgrade, buy_5or10or20_upgrade]

    sum_morethan50 = x[6] + sum_morethan50
    sum_5or10_upgrade = x[7] + sum_5or10_upgrade
    sum_5or10or20_upgrade = x[8] + sum_5or10or20_upgrade

print("所有组合数量= " + str(len(output_lists)))
print("ALL-进度条> 50% 占比 = " + str(sum_morethan50 / len(output_lists)))
print("ALL-再购买个小额礼包(5/10)就可晋级 占比 = " + str(sum_5or10_upgrade / len(output_lists)))
print("ALL-再购买个中小额礼包(5/10/20)就可晋级 占比 = " + str(sum_5or10or20_upgrade / len(output_lists)))
print()

'''
# 几种常见组合输出
always_buy_compose = [

    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 2, 0, 0],
    [2, 1, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1],
    [1, 0, 0, 1, 0],
    [2, 2, 0, 0, 0],
    [1, 2, 0, 0, 0]

]

'''

# 按照规则生成的定的经典情况
# 各个购买 = 1 or 0
# 前两档购买为1到4，其他为0, 且从中去掉前两档都为1的情况
# 第一档为2~4，其他为0
# 第二档为2~4，其他为0

input_lists_config = []
'''
for x1 in [0, 1]:
    for x2 in [0, 1]:
        for x3 in [0, 1]:
            for x4 in [0, 1]:
                for x5 in [0, 1]:
                    list_unit = [x1, x2, x3, x4, x5]
                    input_lists_config.append(list_unit)

for x1 in [1, 2, 3, 4]:
    for x2 in [1, 2, 3, 4]:
        list_unit = [x1, x2, 0, 0, 0]
        input_lists_config.append(list_unit)

for x1 in [2, 3, 4]:
    list_unit = [x1, 0, 0, 0, 0]
    input_lists_config.append(list_unit)

for x2 in [2, 3, 4]:
    list_unit = [0, x2, 0, 0, 0]
    input_lists_config.append(list_unit)

'''

''' 
新的经典规则  - 第一档为0~4，第二档为0~4，其他为0到1
'''

for x1 in [0,1,2,3,4]:
    for x2 in [0,1,2,3,4]:
        for x3 in [0,1]:
            for x4 in [0,1]:
                for x5 in [0,1]:
                    list_unit = [x1, x2, x3, x4, x5]
                    input_lists_config.append(list_unit)
            
# 枚举所有Token情况 与 index ，生成新的输入数组
index_new = 0
input_lists_new = []

# for y in always_buy_compose:
for y in input_lists_config:
    for x in Token:
        # 切片创建新list
        list_new = [index_new, Free[0], x]
        list_new[len(list_new):len(list_new)] = y
        index_new = index_new + 1
        input_lists_new.append(list_new)



# 输出所有常见情况数据

output_lists_new = []

for x in input_lists_new:
    output_unit_new = output_result_list(x)
    output_lists_new.append(output_unit_new)

# 输出所有经典情况的报告
sum_morethan50 = 0
sum_5or10_upgrade = 0
sum_5or10or20_upgrade = 0

for x in output_lists_new:
    # print(x)

    # 汇总的数据为：
    # 所有组合买小额礼包可进档位占比， 所有组合买中小额礼包可进档位占比，所有组合中进度条>50%占比
    # 花费前1/3的人所有组合买小额礼包可进档位占比， 花费前1/3的人所有组合买中中小额礼包可进档位占比，所有组合中进度条>50%占比
    # 数据输出列：[index, sum_tickets, consume_dollar, now_rank, next_rank, percent, if_more_than_50, buy_5or10_upgrade, buy_5or10or20_upgrade]

    sum_morethan50 = x[6] + sum_morethan50
    sum_5or10_upgrade = x[7] + sum_5or10_upgrade
    sum_5or10or20_upgrade = x[8] + sum_5or10or20_upgrade

print("所有组合数量= " + str(len(output_lists_new)))
print("typical-进度条> 50% 占比 = " + str(sum_morethan50 / len(output_lists_new)))
print("typical-再购买个小额礼包(5/10)就可晋级 占比 = " + str(sum_5or10_upgrade / len(output_lists_new)))
print("typical-再购买个中小额礼包(5/10/20)就可晋级 占比 = " + str(sum_5or10or20_upgrade / len(output_lists_new)))
print()



# 将所有常见情况输出打印到csv
# 将数据写入 Csv中 csvCraneOffer
header = ["Index", "Free", "Token", "Gift1", "Gift2", "Gift3", "Gift4", "Gift5","index", "sum_tickets", "consume_dollar", "now_rank", "next_rank", "percent", "if_more_than_50", "buy_5or10_upgrade", "buy_5or10or20_upgrade"]
writer_final = []

for x in range(len(input_lists_new)):
    print_row = []
    print_row.extend(input_lists_new[x])
    print_row.extend(output_lists_new[x])
    # print(print_row)
    writer_final.append(print_row)


with open("csvCraneOffer.csv", "w", newline="") as f:
    ff = csv.writer(f)
    ff.writerow(header)

    ff.writerows(writer_final)
    


