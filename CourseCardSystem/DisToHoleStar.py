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
playerA_lv = 10
playerB_lv = 9

games_cnt = 100000

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


# 函数 LvX的玩家在LvY的场景中随机出杆数
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

    print(" ------ 加载Lv= " + str(playerLv) + " 打Lv= " + str(courseLv) + " 级场权重数据" )
    print("Birde_weight = " + str(birde_weight))
    print("Eagle_weight = " + str(eagle_weight))
    print("Albatross_weight = " + str(albatross_weight))

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



# for game_index in games_cnt:

    # 第一场比赛 A的主场
    # 随机出 A的杆数， 再随机出B的杆数
for game in games_cnt:

