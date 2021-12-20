import xlwings as xw

wb = xw.Book("KingdomSimulator.xlsx")
ws = wb.sheets['Sheet1']

# How to simulate
# Output: log.csv ; Chart

# Tools

''' 常量 '''
import random

min_rank = 1
max_rank = 30
buff_value = 0.20
const_max_shield = 3

''' 常量 '''


''' 工具 - 根据段位获取胜负的点数'''

# 数据容器
win_points_list = [10,20,30]
fail_points_list = [10,20,30]

def Tool_GetPointsDiffbyRank( rank_id,result ):
    '''
    :param rank_id:  int 返回Rank_id
    :param result: bool 输赢
    :return: points_diff: int +/- value
    '''
    if result:
        value_output = win_points_list[rank_id-1]
        print( "rank: " + str(rank_id) + " points + " + str(value_output) )
        return value_output
    else:
        value_output = -fail_points_list[rank_id-1]
        print( "rank: " + str(rank_id) + " change " + str(value_output) )
        return value_output

''' 工具 - 根据连胜获取额外点数 '''

# 数据容器
win_streak_list = [0,2,3]

def Tool_GetExtraPointsbyWinStreak( win_streak ):
    '''
    :param win_streak: int 当前连胜
    :return: extra_points: int 返回的额外点数
    '''
    if win_streak> len(win_streak_list):
        value_output = win_streak_list[len(win_streak_list)-1]
        print("连胜额外点数 : " + str(value_output))
        return  value_output
    else:
        value_output = win_streak_list[win_streak-1]
        print("连胜额外点数 : " + str(value_output))
        return value_output

''' 工具 - 根据当前段位，当前点数，点数增删判断是否触发晋级赛 '''

# 数据容器
tier_upgrade_score = 100

def Tool_GetIfTriggerByRankInfo(now_rank, now_rank_points, points_diff):
    '''
    :param now_rrank: 当前段位
    :param now_rank_points: 当前段位积分
    :param points_diff: 添加积分
    :return: bool True:触发 False: 不触发
    '''
    if now_rank >= max_rank:
        return False
    if now_rank_points + points_diff >=100:
        return True
    else:
        return False

''' 工具 - 根据当前点数，点数增删判断是否触发保级赛'''
tier_delegation_score = 0

def Tool_GetIfDelegationByRankInfo(now_rank, now_rank_points, points_diff):
    '''

    :param now_rank: 当前段位
    :param now_rank_points: 当前段位积分
    :param points_diff: 添加or删减积分
    :return: bool True:触发 False: 不触发
    '''
    if now_rank <= min_rank:
        return False
    if now_rank_points + points_diff <=0:
        return True
    else:
        return False

''' 工具 - 根据总点数返回段位id '''

# 数据容器 - 总点数范围
rank_points_sum_list = [0,100,200,300,400,500]

def Tool_GetRankbyTotalPoints(now_points,promotion_status,delegation_status):
    '''
    :param now_points:  传入的总点数
    :param promotion_status: 是否处于晋级赛
    :param delegation_status: 是否处于保级赛
    :return: int: rankId  返回段位id
    '''
    for index in range(len(rank_points_sum_list)):
        # 当点数等于某一值时，有可能处于两种状态
        if now_points == rank_points_sum_list[index]:
            # 晋级赛，则为下一级
            if promotion_status:
                rankId_output = index
                print("本轮结束后段位id = " + str(rankId_output))
                return rankId_output
            # 保级赛，则为上一级
            if delegation_status:
                rankId_output = index+1
                print("本轮结束后段位id = " + str(rankId_output))
                return rankId_output
            else:
                if index == 0:
                    print("本轮结束后段位id = " + str(index+1))
                    return index+1

        # 当点数不等于某一值时，则判断点数范围
        else:
            # 最后一个段位之外
            if index == len(rank_points_sum_list)-1:
                if now_points > rank_points_sum_list[index]:
                    print("本轮结束后段位id = " + str(index+1))
                    return index+1
            # 在各类段位之中
            if now_points > rank_points_sum_list[index] and now_points < rank_points_sum_list[index+1]:
                print("本轮结束后段位id = " + str(index + 1))
                return index+1

''' 工具 - 根据传入的两方的Bat等级，得出胜负 '''

# 数据容器 - 2维列表
''' [Bat1][Bat2][Bat3][Bat4]...
    [Bat2]
    [Bat3]
    [Bat4]
    ...

'''
WinRateMatrix_list = []

def Tool_GetResultByBatLevel(a_bat_level, b_bat_level):
    '''
    :param a_bat_level: 左方bat等级 - 行号
    :param b_bat_level: 右方bat等级 - 列号
    :return: bool True a胜利 False b胜利
    '''

    a_win_rate = WinRateMatrix_list[a_bat_level-1][b_bat_level-1]
    print(" A vs B win_rate = " + str(a_win_rate))
    random_value = random.random()
    if random_value <= a_win_rate:
        print(" a 获胜 ")
        return True
    else:
        print("b 获胜")
        return False


''' 工具 - 根据传入的 Rank_id 与 Bat等级，返回人数分布 / 每日场数分布 / 编号等'''

# 数据容器  - 2维列表
''' [Bat1][Bat2][Bat3][Bat4]...
    [Kight5]
    [Kight4]
    ...
'''

Distribution_start_list = [] #赛前开始的人数分布 2维list  参数 "distribution"
DailyActive_list = [] #各类玩家的日活 2维list 参数 "dailyActive"
MatchPoolId_list = [] #各类玩家的匹配池编号 2维list 参数 "matchPoolId"

def Tool_GetValueByRankBatLv( rank_id, bat_level, type_string):
    '''
    :param rank_id:  段位id
    :param bat_level:  变幅杆等级
    :param type_string:  distribution/dailyActive/matchPoolId
    :return: 返回相应的值
    '''

    if type_string == "distribution":
        output_value = Distribution_start_list[rank_id-1][bat_level-1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) +  "distrubtion = " + str(output_value))
        return output_value

    if type_string == "dailyActive":
        output_value = Distribution_start_list[rank_id-1][bat_level-1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) +  "dailyActive = " + str(output_value))
        return output_value

    if type_string == "matchPoolId":
        output_value = Distribution_start_list[rank_id-1][bat_level-1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) +  "matchPoolId = " + str(output_value))
        return output_value


# Player
class Player:
    #Attributes

    #初始信息
    id = 0
    origin_rank = 0
    bat_level = 1
    daily_active = 5
    buy_pass = False
    player_type = 1

    #段位&点数
    now_points = 0
    now_rank = 0
    now_rank_points = 0
    total_games_cnt = 0

    #卡*BUFF&连胜
    now_shield = 0
    double_points_card_cnt = 0
    max_shield = const_max_shield

    now_win_streak = 0

    buff_active = False #Buff 是否激活
    now_points_protection_buff = buff_value

    # Mission2  -产出盾牌与双倍卡
    mission2_now_points = 0
    mission2_complete_condition = 0
    mission2_status = False

    # Mission3  -产出Buff
    mission3_now_points = 0
    mission3_complete_condition = 0
    mission3_status = False

    # Log
    points_log_list = []

    # Cache
    diff_points = 0 # 当前比赛缓存点数变化
    next_round_promotion = False  #是否激活晋级赛状态
    next_round_relegation = False #是否激活保级赛状态
    daily_games_cnt_dic = {}

    def __init__(self,  id, origin_rank, daily_active, bat_level, buy_pass):
        self.id = id
        self.origin_rank = origin_rank
        self.bat_level = bat_level
        self.daily_active = daily_active
        self.buy_pass = buy_pass

    def GameSettlement(self, result, day_id):
        '''

        :param result: bool 胜利/失败
        :param day_id: int 第X天

        '''

        ''' 点数增删 '''
        self.points_diff = Tool_GetPointsDiffbyRank(self.now_rank, result)

        # 胜利
        if result == True:

            # 判断双倍卡
            if self.double_points_card_cnt>0:
                # 根据当前段位拿到胜利点数与失败点数
                self.points_diff = self.points_diff*2
                print(" 触发双倍卡 - 点数翻倍为: " + str(self.points_diff))
                self.double_points_card_cnt = self.double_points_card_cnt - 1

            # 判断连胜
            self.now_win_streak = self.now_win_streak + 1
            # 根据连胜判断添加的额外点数
            streak_extra_points = Tool_GetPointsDiffbyRank(self.now_win_streak)
            self.points_diff = self.points_diff + streak_extra_points

            # 判断是否触发晋级赛
            promotion = Tool_GetIfTriggerByRankInfo(self.now_rank, self.now_rank_points,self.points_diff)
            if (promotion):
                self.points_diff = tier_upgrade_score - self.now_points
                self.next_round_promotion = True
                print("这把上分" + str(self.points_diff) + "下一把为晋级赛")
            else:
                self.next_round_promotion = False

        # 失败
        else:
            # 连胜清零
            self.now_win_streak = 0

            # 判断保护盾
            if self.now_shield > 0:
                self.points_diff = 0
                self.now_shield = self.now_shield - 1
                print(" 触发保护盾 - 点数归为 : " + str(self.points_diff))
            # 判断buff
            if self.buff_active:
                self.points_diff = self.points_diff*(1-self.now_points_protection_buff)
                print("触发buff，点数归为：" + str(self.points_diff))

            # 判断是否启动保级赛
            delegation = Tool_GetIfDelegationByRankInfo(self.now_rank, self.now_rank_points, self.points_diff)
            if (delegation):
                self.points_diff = -self.now_rank_points
                self.next_round_relegation = True
                print("这把掉分" + str(self.points_diff) + "下一把为保级赛")

            else:
                self.next_round_relegation = False

        ''' 刷新点数，刷新段位 '''
        # 总点数变化
        self.now_points = self.now_points + self.points_diff
        # 根据总点数刷新段位与now_rank_points
        now_rank = Tool_GetRankbyTotalPoints(self.now_points,self.next_round_promotion,self.next_round_relegation)
        self.now_rank = now_rank


        ''' 时间控制更新 '''
        # 天数变化后当日比赛场数更新，刷新所有任务状态，buff状态
        if str(day_id) in self.daily_games_cnt_dic.keys():
            self.daily_games_cnt_dic[str(day_id)] = self.daily_games_cnt_dic[str(day_id)] + 1
        else:
            self.daily_games_cnt_dic.update({str(day_id): 1})

            self.mission2_status = False
            self.mission3_status = False
            self.buff_active = False

        self.total_games_cnt = self.total_games_cnt + 1


        ''' 刷新所有任务 '''
        if self.mission2_status == False:
            if self.daily_games_cnt_dic[day_id] >= self.mission2_complete_condition:
                self.mission2_status = True
                # 任务2收获奖励，获取双倍卡  or 段位保护卡
                reward_list = ["protect_card", "double_card"]
                reward = mkl_random.choice(reward_list)
                if reward == "protect_card":
                    self.now_shield = self.now_shield + 1
                    print("完成任务2： 获得段位保护卡一张 - 现在总数为：" + str(self.now_shield))
                    if self.now_shield > const_max_shield:
                        self.now_shield = const_max_shield
                        print(" 保护卡超上限，重置为： " + str(self.now_shield))
                else:
                    self.double_points_card_cnt = self.double_points_card_cnt + 1
                    print("完成任务2： 获得段位双倍卡一张 - 现在总数为：" + str(self.double_points_card_cnt))


        if self.buy_pass:
            if self.mission3_status == False:
                if self.daily_games_cnt_dic[day_id] >= self.mission3_complete_condition:
                    # 任务3收获奖励，获取buff
                    self.buff_active = True
                    print("完成任务3：激活buff" )


# 堆栈
class Stack(object):
    ''' 堆栈 '''
    def __init__(self):
        self.items = []

    def is_empty(self):
        '''判断是否为空'''
        return self.items == []

    def push(self, item):
        ''' 加入元素'''
        self.items.append(item)

    def pop(self):
        ''' 弹出元素 '''
        ''' 并返回元素'''
        return self.items.pop()

    def peek(self):
        ''' 返回栈顶元素'''
        return self.items[len(self.items)-1]

    def size(self):
        '''返回栈的大小'''
        return len(self.items)


# MatchPool
class MatchPool:
    '''
    匹配算法的基本数据结构
    '''
    id = 0
    bat_level = 1
    rank_id = 1
    matched_pools_list = [] # 存储对应rank_id 可匹配到的 MatchPool id
    matched_pools_probability = [] # 对应id下匹配到的概率

    #  三堆栈
    stack1_ready_match = Stack()
    stack2_matched = Stack()
    stack3_unActive = Stack()

class FileReader:
    '''
    从Excel中读取各类数据加载到 『数据容器』 中
    方法的包装
    直接调用
    '''
    def __init__(self):
        print("初始化 FileReader")

    # 读取胜率矩阵
    def ReadWinRateMatrix(self):
        '''
        :return:  返回一个2维list ，存储胜率数据
        '''
        # list[index1][index2] index1为行号，index2为列号
        list_outside = []
        row_index_start = 7
        row_index_end = 14
        column_index_start = 4
        column_index_end = 11
        for row in range(row_index_start, row_index_end + 1):
            list_inner = []
            for column in range ( column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row,column)).value)
            list_outside.append(list_inner)

        print("完成胜率矩阵读取")
        for unit in list_outside:
            print(unit)

        return list_outside


    # 读取人数分布矩阵
    def ReadDistributionMatrix(self):
        '''
        :return: 返回一个2维list， 存储人数分布数据
        '''
        list_outside = []
        row_index_start = 20
        row_index_end = 49
        column_index_start = 4
        column_index_end = 11
        for row in range(row_index_start, row_index_end + 1):
            list_inner = []
            for column in range ( column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row,column)).value)
            list_outside.append(list_inner)

        print("完成人数分布矩阵读取")
        for unit in list_outside:
            print(unit)

        return list_outside

    # 读取日活矩阵
    def ReadDailyActiveMatrix(self):
        '''
        :return: 返回一个2维list， 存储日活数据
        '''
        list_outside = []
        row_index_start = 54
        row_index_end = 83
        column_index_start = 4
        column_index_end = 11
        for row in range(row_index_start, row_index_end + 1):
            list_inner = []
            for column in range ( column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row,column)).value)
            list_outside.append(list_inner)

        print("完成日活矩阵读取")
        for unit in list_outside:
            print(unit)

        return list_outside


    # 匹配算法矩阵函数
    def ReadMatchPoolsMatrix(self, input_id):
        '''
        :param input_id:  输入匹配池类的id
        :return: 返回两个list，分别对应该 input_id 下对应的 matched_pool(list) 与 matched_pools_probability(list)
        '''
        list_outside = []
        row_index_start = 88
        row_index_end = 117
        column_index_start = 4
        column_index_end = 11
        for row in range(row_index_start, row_index_end + 1):
            list_inner = []
            for column in range ( column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row,column)).value)
            list_outside.append(list_inner)

        print("完成匹配池ID矩阵读取")
        for unit in list_outside:
            print(unit)

        return list_outside


    # 读取胜利点数/失败点数list
    def ReadWinOrFailPoints(self):
        '''
        :return: 返回2个list，win_points_list， fail_points_list
        '''

    # 读取连胜数据
    def ReadWinStreakPoints(self):
        '''
        :return: 返回1个list, win_streak_list
        '''

    # 读取任务数据
    # 任务条件
    def ReadMissionCondition2(self):
        '''
        :return: 返回1个list, 任务2条件
        '''

    def ReadMissionCondition3(self):
        '''
        :return: 返回1个list, 任务3条件
        '''


test1 = FileReader()
Distribution_start_list = test1.ReadDistributionMatrix()
DailyActive_list = test1.ReadDailyActiveMatrix()
MatchPoolId_list = test1.ReadMatchPoolsMatrix()

a1 = Tool_GetValueByRankBatLv(1,8,"distribution")
a2 = Tool_GetValueByRankBatLv(1,8,"matchPoolId")
a3 = Tool_GetValueByRankBatLv(1,8,"dailyActive")


''' 主循环 
1.读取数据
2.创建好匹配池，创建好玩家
3.根据天数进行匹配
4.返回指标

'''
