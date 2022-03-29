#  枚举所有offer类型并输出为Csv
# Free组合：0，1，2，3 默认为3
# Token组合： 0，1，2，3 可分别计算之
# Gift1组合：0，1，2，3
# Gift2组合：0，1，2，3
# Gift3组合：0，1，2，3
# Gift4组合：0，1，2，3
# Gift5组合：0，1，2，3
# 输出结构 - 2维 List [ [],[],[],... ]
# 每一List为一种组合
# 最后输出为一Csv
# 结构只是简单的循环嵌套而已

import csv

Free = [5]
Token = [0, 1, 2, 3, 5]
Gift1 = [0, 1, 2, 3, 5]
Gift2 = [0, 1, 2, 3, 5]
Gift3 = [0, 1, 2, 3, 5]
Gift4 = [0, 1, 2, 3, 5]
Gift5 = [0, 1, 2, 3, 5]

result = []

for free_unit in Free:
    for Token_unit in Token:
        for Gift5_unit in Gift5:
            for Gift4_unit in Gift4:
                for Gift3_unit in Gift3:
                    for Gift2_unit in Gift2:
                        for Gift1_unit in Gift1:
                            result_unit = [free_unit, Token_unit, Gift1_unit, Gift2_unit, Gift3_unit,
                                           Gift4_unit, Gift5_unit]
                            result.append(result_unit)

# for x in result:
    # print(x)


# 将数据写入 Csv中


header = ["Free", "Token", "Gift1", "Gift2", "Gift3", "Gift4", "Gift5"]
writer_final = []

with open("csvCraneOffer.csv", "w", newline="") as f:
    ff = csv.writer(f)
    ff.writerow(header)

    ff.writerows(result)


