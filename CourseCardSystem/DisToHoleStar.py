import xlwings as xw
import random

wb = xw.Book("CourseCardsSystem.xlsx")
ws = wb.sheets['Sheet1']


# 两位玩家PVP
# 各打一场
# 先随机结果
# 根据结果判定一级胜负
# 记录成绩领先者星星数
# 最后记录胜/负/平

'''
可进一步模拟小胜/中胜/大胜 等各类情况
'''

# 玩家A 与 玩家B
playerA_lv = 9
playerB_lv = 9

games_cnt = 1000

# 定义类 game_record
'''
记录什么？
    games_id 
    
    第一场结果：
        A分数 
        B分数
        A star
        B star
    
    第二场结果：
        A分数 
        B分数
        A star
        B star
    
    最后结果
    1.A_result
    2.B_result
    3.A_star
    4.B_star
    5.最后结果： A胜/B胜/平
        
'''

class GameRecord:

    id = 0

    # 第一场结果
    Record1_ResultA = 0
    Record1_ResultB = 0

    Record1_StarA = 0
    Record1_StarB = 0

    # 第二场结果
    Record2_ResultA = 0
    Record2_ResultB = 0

    Record2_StarA = 0
    Record2_StarB = 0

    # 最后的结果
    A_result = 0
    B_result = 0
    A_star = 0
    B_star = 0


# 根据玩家等级获取相应分数权重数据

# 加载距离星星权重数据


# 函数 LvX的玩家在LvY的场景中随机出各个杆数的权重
def GetWeightPlayerIntoCourse(playerLv, courseLv):
    '''
    :param playerLv:  玩家等级
    :param courseLv:  场景等级
    :return: weight:   Birde,Eagle,Albatross
    '''

    # 玩家Lv 决定列 playerLv + 4
    # 场景Lv 决定行
        # Birde: 4+(courseLv)*3
        # Eagle: 4+(courseLv)*3 + 1
        # ALbatross: 4+(courseLv)*3 + 2

    birde_weight = ws.range( (4+(courseLv)*3, playerLv +4) ).value
    eagle_weight = ws.range( (4+(courseLv)*3 + 1, playerLv +4) ).value
    albatross_weight = ws.range( (4+(courseLv)*3 + 2, playerLv +4) ).value

    '''
    print(" ------ 加载Lv= " + str(playerLv) + " 打Lv= " + str(courseLv) + " 级场权重数据 ------" )
    print("Birde_weight = " + str(birde_weight))
    print("Eagle_weight = " + str(eagle_weight))
    print("Albatross_weight = " + str(albatross_weight))

    print(" ------ 权重随机END ------- ")
    print("")
    '''

    result_list = [birde_weight,eagle_weight,albatross_weight]
    return result_list

GetWeightPlayerIntoCourse(3,4)

# 函数 根据权重返回Index
def GetRandomResultByWeight(weight_list):
    '''
    :param weight_list: 权重列表
    :return: 返回index
    '''
    _total = sum(weight_list)
    _random = random.uniform(0,_total)
    _curr_sum = 0
    _ret = None


    index = -1
    for x in weight_list:
        index = index + 1
        _curr_sum += x
        if _random <= _curr_sum:
            _ret = index
            break

    print("按照权重随机  result_index = " + str(_ret))
    return _ret


# 函数 根据胜利杆数按照权重随机出距离并获得星星
def GetStarByRandomDistance(result):

    # 根据结果index选择不同的随机区间
    # 0 Birde weight-18 & star-17
    # 1 Eagle weight-22 & star-21
    # 2 Albatross weight-26 & star-25

    # Birde
    if result == 0:
        row_index = 3
        dis_weight_list = []
        while ws.range((row_index, 18)).value !=None:
            dis_weight_list.append(ws.range((row_index, 18)).value)
            row_index = row_index + 1
        index_output = GetRandomResultByWeight(dis_weight_list)

        star_result = ws.range((index_output + 3, 17)).value
        print(" birde " + " dis < " + str(ws.range((index_output+3, 16)).value) + " star = " + str(star_result))

        return star_result

    # Eagle
    if result == 1:
        row_index = 3
        dis_weight_list = []
        while ws.range((row_index, 22)).value != None:
            dis_weight_list.append(ws.range((row_index, 22)).value)
            row_index = row_index + 1
        index_output = GetRandomResultByWeight(dis_weight_list)

        star_result = ws.range((index_output + 3, 21)).value
        print(" eagle " + " dis < " + str(ws.range((index_output+3, 20)).value) + " star = " + str(star_result))

        return star_result

    # Albatross
    if result == 2:
        row_index = 3
        dis_weight_list = []
        while ws.range((row_index, 26)).value != None:
            dis_weight_list.append(ws.range((row_index, 26)).value)
            row_index = row_index + 1
        index_output = GetRandomResultByWeight(dis_weight_list)

        star_result = ws.range((index_output + 3, 25)).value
        print(" albatross " + " dis < " + str(ws.range((index_output+3, 24)).value) + " star = " + str(star_result))

        return star_result


tie_cnt = 0

for game_index in range(games_cnt):

    print("")
    print(" ----- 开始第 " + str(game_index) + " 场比赛 ----- ")
    print(" 第一局比赛 A主场 ")

    # 第一场比赛 A的主场
    # 随机出 A的杆数， 再随机出B的杆数

    # 0 Birde
    # 1 Eagle
    # 2 Albatross

    a_score = 0
    b_score = 0
    a_star = 0
    b_star = 0


    a_result_1 = GetRandomResultByWeight(GetWeightPlayerIntoCourse(playerA_lv, playerA_lv))
    b_result_1 = GetRandomResultByWeight(GetWeightPlayerIntoCourse(playerB_lv, playerA_lv))
    a_star_1 = GetStarByRandomDistance(a_result_1)
    b_star_1 = GetStarByRandomDistance(b_result_1)

    if a_result_1 == b_result_1:
        a_score = a_score + 0.5
        b_score = b_score + 0.5
        a_star = a_star + a_star_1
        b_star = b_star + b_star_1

        print("平局" + "0.5 : 0.5 " + " star " + str(a_star_1) + " : " + str(b_star_1) )

    else:
        if a_result_1 > b_result_1:
            a_score = a_score + 1
            a_star = a_star + a_star_1

            print("A胜利" + "1 : 0.5 " + " star " + str(a_star_1) + " : " + str(b_star_1))

        if a_result_1 < b_result_1:
            b_score = b_score + 1
            b_star = b_star + b_star_1

            print("B胜利" + "0.5 : 1 " + " star " + str(a_star_1) + " : " + str(b_star_1))


    print(" 第一局比赛结束")
    print(" A score = " + str(a_score) + " A star = " + str(a_star))
    print(" B score = " + str(b_score) + " B star = " + str(b_star))
    print("")

    print(" 第二局比赛 B主场 ")

    a_result_2 = GetRandomResultByWeight(GetWeightPlayerIntoCourse(playerA_lv, playerB_lv))
    b_result_2 = GetRandomResultByWeight(GetWeightPlayerIntoCourse(playerB_lv, playerB_lv))
    a_star_2 = GetStarByRandomDistance(a_result_2)
    b_star_2 = GetStarByRandomDistance(b_result_2)

    if a_result_2 == b_result_2:
        a_score = a_score + 0.5
        b_score = b_score + 0.5
        a_star = a_star + a_star_2
        b_star = b_star + b_star_2

        print("平局" + "0.5 : 0.5 " + " star " + str(a_star_2) + " : " + str(b_star_2) )

    else:
        if a_result_2 > b_result_2:
            a_score = a_score + 1
            a_star = a_star + a_star_2

            print("A胜利" + "1 : 0.5 " + " star " + str(a_star_2) + " : " + str(b_star_2))


        if a_result_2 < b_result_2:
            b_score = b_score + 1
            b_star = b_star + b_star_2

            print("B胜利" + "0.5 : 1 " + " star " + str(a_star_2) + " : " + str(b_star_2))

    print(" 第二局比赛结束")
    print(" A score = " + str(a_score) + " A star = " + str(a_star))
    print(" B score = " + str(b_score) + " B star = " + str(b_star))

    if a_score > b_score:
        print (" A 胜利  - 比分胜利 ")
    if b_score > a_score:
        print (" B 胜利  - 比分胜利 ")
    if a_score == b_score:
        if a_star > b_star:
            print(" A 胜利  - 星星胜利 ")
        if b_star > a_star:
            print(" B 胜利  - 星星胜利 ")
        if a_star == b_star:
            print(" 平局 - 比分一致 ， 星星一致 ")
            tie_cnt = tie_cnt + 1

    print(" ----- 第 " + str(game_index) + " 场比赛结束----- ")
    print("")

tie_rate  = tie_cnt /games_cnt
print(" 平均率 = " + str(tie_rate))


