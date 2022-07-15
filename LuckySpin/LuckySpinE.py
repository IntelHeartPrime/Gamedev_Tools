''' 计算LuckySpin期望值 '''
items_pool1 = [
    "legen_chip",
    "coin1",
    "diamond",
    "ball1",
    "card1",
    "coin2",
    "ball2",
    "coinOrCard"
]

container_combination = []

index = 0
for x1 in items_pool1:
    # 从items_pool 剔除 x1
    items_cache1 = items_pool1.copy()
    items_cache1.remove(x1)
    for x2 in items_cache1:
        items_cache2 = items_cache1.copy()
        items_cache2.remove(x2)
        for x3 in items_cache2:
            items_cache3 = items_cache2.copy()
            items_cache3.remove(x3)
            for x4 in items_cache3:
                items_cache4 = items_cache3.copy()
                items_cache4.remove(x4)
                for x5 in items_cache4:
                    items_cache5 = items_cache4.copy()
                    items_cache5.remove(x5)
                    for x6 in items_cache5:
                        items_cache6 = items_cache5.copy()
                        items_cache6.remove(x6)
                        for x7 in items_cache6:
                            items_cache7 = items_cache6.copy()
                            items_cache7.remove(x7)
                            print(items_cache7)
                            x8 = items_cache7[0]
                            index += 1
                            list1 = [x1,x2,x3,x4,x5,x6,x7,x8]
                            print(" index " + str(index) + " -- " + str(list1))
                            container_combination.append(list1)


''' 函数，读表，读取权重变化矩阵 '''
Weight_Matrix = []     # 二维list
Weight_Matrix_use = [] # 二维list ，每次的每个物品为一个list

import xlwings as xw
wb = xw.Book("LuckySpinSystem.xlsx")
ws1 = wb.sheets['Sheet1']

def ReadWeightMatrix():
    row_start = 4
    col_start = 4

    for x in range(4,12):
        list_cache = []
        for y in range(4,12):
            list_cache.append(int(ws1.range((x, y)).value))

        Weight_Matrix.append(list_cache)

    print(" --- 开始读取权重矩阵 ---")
    for unit in Weight_Matrix:
        print(unit)
    print(" --- 读取权重矩阵完毕 ---")

    for y in range(4,12):
        list_cache = []
        for x in range(4,12):
            list_cache.append(int(ws1.range((x, y)).value))

        Weight_Matrix_use.append(list_cache)

    print(" --- 开始读取权重矩阵 ---")
    for unit in Weight_Matrix:
        print(unit)
    print(" --- 读取权重矩阵完毕 ---")

    print(" --- 开始读取权重矩阵 use ---")
    for unit in Weight_Matrix_use:
        print(unit)
    print(" --- 读取权重矩阵完毕user ---")


ReadWeightMatrix()

''' 函数，传入list，计算此条组合概率 '''
def Cal_sampleProbability( sample ):
    '''
    :param sample: 传入的组合list  比如：['coinOrCard', 'ball2', 'coin2', 'card1', 'coin1', 'ball1', 'diamond', 'legen_chip']['ball1']
    :return: 抽到概率
    '''

    p_cache = []

    inOrOutPool = [1, 1, 1, 1, 1, 1, 1, 1]  # 1 表示对应位置能抽到，0表示抽不到
    for x in range(len(sample)):

        item_index = None
        #定位所抽到的物品对应的index
        for index in range(len(items_pool1)):
            if sample[x] == items_pool1[index]:
                item_index = index


        print("第 " + str(x+1) +  " 次抽取" + " 抽取到 " + str(sample[x]))
        #获取最新的权重list
        weight_cache = Weight_Matrix_use[x]
        print("原始权重列表 = " + str(weight_cache))
        print(" lock = " + str(inOrOutPool))

        #计算本次抽取概率
        weight_sum = 0
        for y in range(len(inOrOutPool)):
            lock = inOrOutPool[y]
            if lock == 1:
                weight_sum = weight_sum + weight_cache[y]
        print("总权重 = " + str(weight_sum))

        #抽到的物品所代表的权重
        weight_picked_item = weight_cache[item_index]
        print(" 抽到物品权重 = " + str(weight_picked_item))

        # 计算本次概率
        picked_p = weight_picked_item / weight_sum
        p_cache.append(picked_p)

        # 能抽到的开关调整
        inOrOutPool[item_index] = 0

    # 计算概率
    print(" 各次概率 = " + str(p_cache))
    p_multiply = 1.0000000
    for v in p_cache:
        p_multiply = p_multiply * v

    print( "最后概率 = " + str(p_multiply))
    return p_multiply

t = 0
p_sum = 0.0000
p_container = []
for c in container_combination:
    t += 1
    print()
    print(" --- 运算 第 " + str(t) + " 次组合 --- ")
    p = Cal_sampleProbability(c)
    p_container.append(p)
    p_sum = p_sum + p

# 验证环节
print( "p_sum = " + str(p_sum))


e_container = []

''' 最后，计算抽到各个物品的期望次数 '''
for i in range(len(items_pool1)):

    e_value = 0.000

    item = items_pool1[i]
    print(" 开始计算物品 " + str(item) + " 的期望次数 ")

    for l in range(len(container_combination)):
        list_c = container_combination[l]
        p_cal = p_container[l]
        for c in range(len(list_c)):
            if item == list_c[c]:
                time_cal = c + 1
                e_cal = p_cal * time_cal
                print("第 " + str(time_cal) + " 次抽到 " + str(item) + " 概率 = " + str(p_cal) + " e = " + str(e_cal))
                e_value = e_value + e_cal

    print("最后物品 " + str(item) + " 期望次数 = " + str(e_value))
    e_container.append(e_value)

for i in range(len(e_container)):
    item = items_pool1[i]
    e = e_container[i]

    ws1.range((4+i, 12)).value = e
    print(str(item) + "," + str(e))

# 将结果输入到Excel中
