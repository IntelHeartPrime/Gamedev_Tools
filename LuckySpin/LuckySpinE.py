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

''' 函数，读表，读取权重变化矩阵 '''


''' 函数，传入list，计算此条组合概率 '''


''' 最后，计算抽到各个物品的期望次数 '''