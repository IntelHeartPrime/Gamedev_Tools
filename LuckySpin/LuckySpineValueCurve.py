# 此命名空间也用于 LuckySpinSimulator 中

import random

# 抽取操作
# 开启一轮抽取
# 开启第x次抽取
# 根据权重抽取，抽取后将标识设置为False
# 记录每个位置的价值



import xlwings as xw
wb = xw.Book("LuckySpinSystem.xlsx")
ws = wb.sheets['s11s12']


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
            weight_list.append(gift.weight)



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

        if i < len(sum_list) - 1:
            if i == 0:
                if random_w <= sum_list[i]:
                    picked_index = i
            if (random_w > sum_list[i]) and (random_w <= sum_list[i+1]):
                picked_index = i + 1
        if i == (len(sum_list) - 1):
            if random_w >= sum_list [i]:
                picked_index = i

        # 只剩下一个对象
        if len(sum_list) == 1:
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

    return picked_gift_index


''' 准备数据 '''
index = [0,1,2,3,4,5,6,7]
weightMatrix = []      # 2维数组，代表每一次的权重list
nameList = [] # 名称
valueList = []  # 价值比例

value_sum = [0,0,0,0,0,0,0,0]

for c in range(5, 12+1):
    weight_c = []
    for r in range(4, 11+1):
        weight_c.append( int(ws.range((r,c)).value))
    weightMatrix.append(weight_c)

print("weight Matrix : ")
for w in weightMatrix:
    print(w)
print()

for r in range(4, 11+1):
    nameList.append(ws.range((r, 3)).value)
    valueList.append(ws.range((r,2)).value)

print("Name:")
print(nameList)
print("Value:")
print(valueList)

times = 10000
for x in range(times):
    print(" --- 这是第 " + str(x+1) + " 轮抽取 ---")

    # 创建 gift_list
    gift_list = []
    for i in range(len(index)):
        g1 = Gift()
        g1.index = index[i]
        g1.lock = True
        gift_list.append(g1)

    # 从weightMatrix 读取 weigh_list
    for y in range(8):
        print("--- 这一轮中，第" + str(y+1) + "次抽取操作 --- ")
        w_list = weightMatrix[y]
        for g in range(len(gift_list)):
            gift_list[g].weight = w_list[g]

        # 开始抽取
        pickedItemIndex = RandomAnItem(gift_list)
        value_sum[y] += valueList[pickedItemIndex]

        print()

ave_value = []
for v in value_sum:
    ave_v = v / times
    ave_value.append(ave_v)

print(ave_value)

# 将ave_value 写入到Excel中
for c in range(5,12+1):
    ws.range((25,c)).value = ave_value[c-5]


'''
# unit test code 
index = [0,1,2,3,4,5,6,7]
weight = [100,100,100,100,100,100,100,100]

times_sum = [0,0,0,0,0,0,0,0]

#随机能力正确性验证
for t in range(10000):

    gift_test = []
    for i in range(len(index)):
        g1 = Gift()
        g1.index = index[i]
        g1.weight = weight[i]
        g1.lock = True

        gift_test.append(g1)

    item_index = RandomAnItem(gift_test)
    for i in range(len(index)):
        if i == item_index:
            times_sum[i] += 1

print(times_sum)
'''