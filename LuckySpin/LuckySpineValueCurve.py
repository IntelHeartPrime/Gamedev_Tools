# 此命名空间也用于 LuckySpinSimulator 中

import random

''' 连续抽取 10000轮， 计算每次的平均价值 '''


''' 计算法 '''
''' 树连乘计算价值 '''

''' 暴力法之后和权重计算法比较即可 '''

# 抽取操作
# 开启一轮抽取
# 开启第x次抽取
# 根据权重抽取，抽取后将标识设置为False
# 记录每个位置的价值


import xlwings as xw
wb = xw.Book("LuckySpinSystem.xlsx")
ws1 = wb.sheets['整理']

class Gift:
    def __init__(self):
        self.index = 0  # 对应在固定物品列表中的索引
        self.weight = 0 # 本次权重
        self.lock = True # 可被随到True, 不可被随到 False


''' func - 根据传入的权重list & lock list 进行抽取 '''
def RandomAnItem( gift_list ):
    '''
    :param gift_list 物品类id
    :return: item_id 被抽到的物品index , 并将gift_list值刷新
    '''
    print("RandomAnItem Start ")

    index_list = []
    weight_list = []
    sum_list = []

    for gift in gift_list:
        if gift.lock:
            index_list.append(gift.index)
            weight_list.append(weight_list)

    if len(index_list) <= 0:
        print("物品已被抽完")
        raise ValueError

    # 求总权重
    w_sum = 0
    for w in weight_list:
        w_sum += w
        sum_list.append(w_sum)

    print("sum_list = " + str(sum_list))

    # 随出一个数
    picked_index = None

    random_w = random.randint(0, w_sum)
    print(" random_w = " + str(random_w))
    for i in range(len(sum_list)):

        if i < len(sum_list):
            if i == 0:
                if random_w <= sum_list[i]:
                    picked_index = i
            if random_w > sum_list[i] and random_w < sum[i+1]:
                picked_index = i + 1
        if i == len(sum_list):
            if random_w >= sum_list [i]:
                picked_index = i

        print("picked_index = " + str(picked_index))

    if picked_index == None:
        print(" 没抽到任何物品 ")
        raise ValueError

    picked_gift_index = index_list[picked_index]
    print("抽到id = " + str(picked_gift_index) +  "的物品")

    # gift_list 内状态改变
    for gift in gift_list:
        if gift.index == picked_gift_index:
            gift.lock = False

    return  picked_gift_index



'''
times = 10000
for x in range(times):
    print(" --- 这是第 " + str(x+1) + " 轮抽取 ---")
    for y in range(8):
        print("--- 这一轮中，第" + str(y+1) + "次抽取操作 --- ")
'''

# unit test
