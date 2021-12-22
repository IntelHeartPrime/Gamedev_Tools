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

tier_upgrade_score = 100
tier_delegation_score = 0

''' 常量 '''

# 数据容器 ########################
win_points_list = [10, 20, 30]  # 胜利获得点数
fail_points_list = [10, 20, 30]  # 失败获得点数

win_streak_list = [0, 2, 3]  # 连胜获得点数

rank_points_sum_list = [0, 100, 200, 300, 400, 500]  # rankid对应总点数

''' [Bat1][Bat2][Bat3][Bat4]...
    [Bat2]
    [Bat3]
    [Bat4]
    ...

'''
WinRateMatrix_list = []

''' [Bat1][Bat2][Bat3][Bat4]...
    [Kight5]
    [Kight4]
    ...
'''

Distribution_start_list = []  # 赛前开始的人数分布 2维list  参数 "distribution"
DailyActive_list = []  # 各类玩家的日活 2维list 参数 "dailyActive"
MatchPoolId_list = []  # 各类玩家的匹配池编号 2维list 参数 "matchPoolId"

Mission2Condition = []
Mission3Condition = []

matchPools = []  # 单元为matchPool的list
##################################


''' 工具 - 根据晋级 or 掉级 将相应的player 移动到对应的 matchPools中'''


def Tool_MovePlayerToMatchPools(player, promotionOrRelegation):
    '''
    :param player: 传入的player对象
    :param promotionOrRelegation: True，代表晋级； False，代表掉段
    :return: None
    '''
    rank_id = player.now_rank
    bat_level = player.bat_level

    player.moved = True
    # 晋级
    if promotionOrRelegation:
        if rank_id > 30:
            rank_id = 30
        matchpool_id = MatchPoolId_list[rank_id - 1][bat_level - 1]
        matchPools[int(matchpool_id) - 1].stack1_ready_match.items.append(player)

        print("【晋级移动】玩家 player_id = " + str(player.id) + "   origin_rank = " + str(
            player.origin_rank) + " now_rank = " + str(player.now_rank) + " bat_level = " + str(
            player.bat_level) + " 的玩家移动到 matchPoolId为" + str(matchpool_id) + " 的匹配池")
        return None
    else:
        if rank_id < 1:
            rank_id = 1
        matchpool_id = MatchPoolId_list[rank_id - 1][bat_level - 1]
        matchPools[int(matchpool_id) - 1].stack1_ready_match.items.append(player)
        print("【降级移动】玩家 player_id = " + str(player.id) + "origin_rank = " + str(
            player.origin_rank) + " now_rank = " + str(player.now_rank) + " bat_level = " + str(
            player.bat_level) + " 的玩家移动到 matchPoolId为" + str(matchpool_id) + " 的匹配池")
        return None


''' 工具 - 传入对象到特定的id的matchPoolUnit的matched_stack中  用于晋级/掉级'''


def Tool_PushItemIntoStackByMatchPoolId(matchPoolId, player):
    '''
    依赖数据容器 matchPools
    :param matchPoolId: 对应的matchPoolId
    :param player: 传入的player对象
    :return: None
    '''
    matchPools[matchPoolId - 1].stack2_matched.pop(player)


''' 工具 - 返回Stack中player状态为ready_match 的人数'''


def Tool_GetPlayerCntfromStack(matchPoolId):
    num = matchPools[int(matchPoolId - 1)].stack1_ready_match.getSumReadyMatchPlayer()
    print("匹配池" + str(matchPoolId) + " 中的活跃玩家有 " + str(num) + "个")
    return num


''' 工具 - 匹配函数 - 根据传入的matchUnit对象返回匹配到的matchUnitId'''


def Tool_GetMatchResult(player, matchPoolId):
    '''
    :param player: 传入的player对象
    :param matchPoolId: 需要匹配的matchPoolId
    :return: output_id : int 匹配到的matchPoolId
    '''
    # 获取能匹配到的id列表
    # 获取对应的概率列表
    # 筛选掉人数不够的匹配池

    matched_pools_list = matchPools[matchPoolId - 1].matched_pools_list
    matched_pools_probability = matchPools[matchPoolId - 1].matched_pools_probability

    matched_pools_list_new = []
    matched_pools_probability_new = []
    index = 0
    for id in matched_pools_list:
        len_list = Tool_GetPlayerCntfromStack(id)
        if len_list >= 1:
            # 当传入的playerid与对应的matchPool下的 batLv & rank_id 对应时，且数量=1 ，则排除此list
            rank_id_c, bat_lv_c = Tool_GetRankIdBatLvByMatchPoolId(id)
            if (player.now_rank == rank_id_c and player.bat_level == bat_lv_c and len_list == 1) == False:
                matched_pools_list_new.append(id)
                matched_pools_probability_new.append(matched_pools_probability[index])
        index = index + 1

    if len(matched_pools_list_new) < 1:
        print("匹配不到任何玩家")
        return None
    else:
        # 随机出结果并输出
        return Tool_GetRandomItemByWeight(matched_pools_list_new, matched_pools_probability_new)


''' 工具 - 按照传入的id_list, weight_list 随机选择1个id输出 '''


def Tool_GetRandomItemByWeight(id_list, weight_list):
    '''
    :param id_list: list 传入的id列表，从中按照权重选择一个值
    :param weight_list: 权重列表
    :return: id :int 返回匹配池id
    '''

    if (len(id_list)) > 1:
        output_value = random.choices(id_list, weights=weight_list, k=1)
        print("匹配到 " + str(output_value))
        return output_value[0]
    elif len((id_list)) == 1:
        output_value = id_list[0]
        print("匹配到 " + str(output_value))
        return output_value
    else:
        print("匹配不到任何")
        return None


''' 工具 - 返回所有DailyActive中的最大值 '''


def Tool_GetMaxValueDailyActive():
    max_value = 0
    for x in DailyActive_list:
        for y in x:
            if y > max_value:
                max_value = y
    print(" 最大帧数 = " + str(max_value))
    return max_value


''' 工具 - 根据段位获取胜负的点数'''


def Tool_GetPointsDiffbyRank(rank_id, result):
    '''
    :param rank_id:  int 返回Rank_id
    :param result: bool 输赢
    :return: points_diff: int +/- value
    '''
    if result:
        value_output = win_points_list[rank_id - 1]
        print("rank: " + str(rank_id) + " points + " + str(value_output))
        return value_output
    else:

        value_output = -fail_points_list[rank_id - 1]
        print("rank: " + str(rank_id) + " change " + str(value_output))
        return value_output


''' 工具 - 根据连胜获取额外点数 '''


def Tool_GetExtraPointsbyWinStreak(win_streak):
    '''
    :param win_streak: int 当前连胜
    :return: extra_points: int 返回的额外点数
    '''
    if win_streak > len(win_streak_list):
        value_output = win_streak_list[len(win_streak_list) - 1]
        print("连胜额外点数 : " + str(value_output))
        return value_output
    else:
        value_output = win_streak_list[win_streak - 1]
        print("连胜额外点数 : " + str(value_output))
        return value_output


''' 工具 - 根据当前段位，当前点数，点数增删判断是否触发晋级赛 '''


def Tool_GetIfTriggerByRankInfo(now_rank, now_rank_points, points_diff):
    '''
    :param now_rank: 当前段位
    :param now_rank_points: 当前段位积分
    :param points_diff: 添加积分
    :return: bool True:触发 False: 不触发
    '''
    if now_rank >= max_rank:
        return False
    if now_rank_points + points_diff >= 100:
        return True
    else:
        return False


''' 工具 - 根据当前点数，点数增删判断是否触发保级赛'''


def Tool_GetIfDelegationByRankInfo(now_rank, now_rank_points, points_diff):
    '''

    :param now_rank: 当前段位
    :param now_rank_points: 当前段位积分
    :param points_diff: 添加or删减积分
    :return: bool True:触发 False: 不触发
    '''
    if now_rank <= min_rank:
        return False
    if now_rank_points + points_diff <= 0:
        return True
    else:
        return False


''' 工具 - 根据总点数返回段位id '''


def Tool_GetRankbyTotalPoints(now_points, promotion_status, delegation_status):
    '''
    :param now_points:  传入的总点数
    :param promotion_status: 是否处于晋级赛
    :param delegation_status: 是否处于保级赛
    :return: int: rankId  返回段位id
    '''
    print(" 参数now_points = " + str(now_points) + " 参数 promotion_status= " + str(
        promotion_status) + " 参数 delegation_status = " + str(delegation_status))

    for index in range(len(rank_points_sum_list)):
        # 当点数等于某一值时，有可能处于两种状态
        if now_points == rank_points_sum_list[index]:
            # 晋级赛，则为下一级
            if promotion_status:
                rankId_output = index
                print("当前处于 晋级赛 状态，本轮结束后段位id = " + str(rankId_output))
                if rankId_output == 0:
                    print(" 危 " + " 参数now_points = " + str(now_points) + " 参数 promotion_status= " + str(
                        promotion_status) + " 参数 delegation_status = " + str(delegation_status))
                return rankId_output
            # 保级赛，则为上一级
            if delegation_status:
                rankId_output = index + 1
                print("当前处于 保级赛 状态，本轮结束后段位id = " + str(rankId_output))
                return rankId_output
            else:
                if index == 0:
                    print("本轮结束后段位id = " + str(index + 1))
                    return index + 1

        # 当点数不等于某一值时，则判断点数范围
        else:
            # 最后一个段位之外
            if index == len(rank_points_sum_list) - 1:
                if now_points > rank_points_sum_list[index]:
                    print("本轮结束后段位id = " + str(index + 1))
                    return index + 1
            # 在各类段位之中
            if now_points > rank_points_sum_list[index] and now_points < rank_points_sum_list[index + 1]:
                print("本轮结束后段位id = " + str(index + 1))
                return index + 1


''' 工具 - 根据传入的当前总点数，当前段位id，得出当前段位点数'''


def Tool_GetNowRankPoints(sum_points, now_rank):
    '''
    :param sum_points: int 当前总点数
    :param now_rank: int 当前段位id
    :return: now_rank_points: 当前段位点数
    '''
    output_value = sum_points - rank_points_sum_list[int(now_rank) - 1]
    print("当前段位点数 = " + str(output_value))
    return output_value


''' 工具 - 根据传入的两方的Bat等级，得出胜负 '''


def Tool_GetResultByBatLevel(a_bat_level, b_bat_level):
    '''
    :param a_bat_level: 左方bat等级 - 行号
    :param b_bat_level: 右方bat等级 - 列号
    :return: bool True a胜利 False b胜利
    '''

    a_win_rate = WinRateMatrix_list[int(a_bat_level) - 1][int(b_bat_level) - 1]
    print(" A vs B win_rate = " + str(a_win_rate))
    random_value = random.random()
    if random_value <= a_win_rate:
        print(" a 获胜 ")
        return True
    else:
        print("b 获胜")
        return False


''' 工具 - 根据传入的 Rank_id 与 Bat等级，返回人数分布 / 每日场数分布 / 编号等'''


def Tool_GetValueByRankBatLv(rank_id, bat_level, type_string):
    '''
    :param rank_id:  段位id
    :param bat_level:  变幅杆等级
    :param type_string:  distribution/dailyActive/matchPoolId
    :return: 返回相应的值
    '''

    if type_string == "distribution":
        output_value = Distribution_start_list[rank_id - 1][bat_level - 1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) + " distriubtion = " + str(output_value))
        return output_value

    if type_string == "dailyActive":
        output_value = DailyActive_list[rank_id - 1][bat_level - 1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) + " dailyActive = " + str(output_value))
        return output_value

    if type_string == "matchPoolId":
        output_value = MatchPoolId_list[rank_id - 1][bat_level - 1]
        print("rank_id  =" + str(rank_id) + " bat_level = " + str(bat_level) + " matchPoolId = " + str(output_value))
        return output_value


''' 工具 - 根据传入的RankId 返回对应的任务2完成条件 '''


def Tool_GetConditionbyRank2(rank_id):
    print("rank_id = " + str(rank_id) + " mission2_condition = " + str(Mission2Condition[rank_id - 1]))
    return Mission2Condition[rank_id - 1]


''' 工具 - 根据传入的RankId 返回对应的任务3完成条件 '''


def Tool_GetConditionbyRank3(rank_id):
    print("rank_id = " + str(rank_id) + " mission3_condition = " + str(Mission3Condition[rank_id - 1]))
    return Mission3Condition[rank_id - 1]


''' 工具 - 根据MatchPoolId 返回其 rank_id 与 bat_level '''


def Tool_GetRankIdBatLvByMatchPoolId(MatchPoolId):
    '''
    :param MatchPoolId: 匹配池id
    :return: rank_id ; bat_level
    '''
    bat_level = MatchPoolId % 8
    rank_id = (MatchPoolId // 8) + 1

    return rank_id, bat_level


''' 工具 - 根据输入的MatchPoolId，返回其可匹配到MatchPool以及对应概率'''


def Tool_GetMatchPoolProbabilitybyId(MatchPoolId):
    '''
    :param MatchPoolId: 匹配池id
    :return: MatchPoolId_list : list 能匹配到的MatchPool 的id ；  Probability_list : list
    '''
    rank_id, bat_level = Tool_GetRankIdBatLvByMatchPoolId(MatchPoolId)

    MatchPool_list = []
    Probability_list = []

    rank_id_left = rank_id - 1
    rank_id_right = rank_id + 1
    bat_level_left = bat_level - 1
    bat_level_right = bat_level + 1
    if rank_id_left < 1:
        rank_id_left = 1
    if rank_id_right > 30:
        rank_id_right = 30
    if bat_level_left < 1:
        bat_level_left = 1
    if bat_level_right > 8:
        bat_level_right = 8
    for lv in range(bat_level_left, bat_level_right + 1):
        for rank in range(rank_id_left, rank_id_right):
            pool_id = Tool_GetValueByRankBatLv(rank, lv, "matchPoolId")
            MatchPool_list.append(pool_id)
            # 概率计算
            num1 = abs(lv - bat_level)
            num2 = abs(rank - rank_id)
            num_para = num1 + num2
            if num_para == 0:
                Probability_list.append(0.4)
            if num_para == 1:
                Probability_list.append(0.1)
            if num_para == 2:
                Probability_list.append(0.05)
    print("MatchPoolId = " + str(MatchPoolId) + " rank_id = " + str(rank_id) + " bat_level = " + str(
        bat_level) + " 的玩家能匹配到：")
    print(MatchPool_list)
    print("概率 = " + str(Probability_list))

    return MatchPool_list, Probability_list


# Player
class Player:
    # Attributes

    # 特殊功能开关
    function_lock = True

    player_status = "ready_match"  # ready_match / matched / unactive
    # 初始信息
    id = 0
    origin_rank = 0
    bat_level = 1
    daily_active = 5
    buy_pass = False
    player_type = 1

    # 段位&点数
    now_points = 0
    now_rank = 0
    now_rank_points = 0
    total_games_cnt = 0

    # 卡*BUFF&连胜
    now_shield = 0
    double_points_card_cnt = 0
    max_shield = const_max_shield

    now_win_streak = 0

    buff_active = False  # Buff 是否激活
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
    diff_points = 0  # 当前比赛缓存点数变化
    next_round_promotion = False  # 是否激活晋级赛状态
    next_round_relegation = False  # 是否激活保级赛状态
    daily_games_cnt_dic = {}

    promotion_victory = False
    relegation_victory = False

    moved = False

    def __init__(self, id, origin_rank, daily_active, bat_level, buy_pass):
        self.id = id
        self.origin_rank = origin_rank
        self.now_rank = origin_rank

        self.bat_level = bat_level
        self.daily_active = daily_active
        self.buy_pass = buy_pass

        self.now_points = rank_points_sum_list[int(origin_rank) - 1] + 20
        self.now_rank_points = 20
        self.daily_games_cnt_dic = {}

    def GameSettlement(self, result, day_id, frame_id):
        '''

        :param result: bool 胜利/失败
        :param day_id: int 第X天
        :pram frame_id: int 第x帧

        '''

        ''' 时间控制更新 '''
        # 天数变化后当日比赛场数更新，刷新所有任务状态，buff状态
        if str(day_id) in self.daily_games_cnt_dic.keys():
            print("日 " + str(day_id) + " 活跃+ 1")
            self.daily_games_cnt_dic[str(day_id)] = self.daily_games_cnt_dic[str(day_id)] + 1
        else:
            self.daily_games_cnt_dic.update({str(day_id): 1})
            print("新的一天 -" + str(day_id) + "刷新重置所有任务状态")
            self.mission2_status = False
            self.mission3_status = False
            self.buff_active = False

        ''' 点数增删 '''

        # 打印战斗前点数
        print("")
        print("第[" + str(day_id) + "】天战斗" + " 第 [" + str(frame_id) + "]帧 id = " + str(self.id) + " 玩家原始段位 = " + str(
            self.origin_rank) + " 玩家当前段位 = " + str(self.now_rank) + " 玩家战斗前总点数 = " + str(
            self.now_points) + " 玩家当前段位点数 = " + str(self.now_rank_points))
        print("当前护盾数 = " + str(self.now_shield) + " 当前双倍卡数 = " + str(self.double_points_card_cnt))

        print("当其buff状态 = " + str(self.buff_active))
        print(" 本局开始之前 " + "晋级赛？ " + str(self.next_round_promotion) + " 保级赛？ " + str(self.next_round_relegation))
        print("")

        self.points_diff = Tool_GetPointsDiffbyRank(self.now_rank, result)

        # 胜利
        if result == True:
            self.next_round_relegation = False

            # 判断是否是晋级赛
            if self.next_round_promotion:
                # 是
                self.next_round_promotion = False

                if self.function_lock:
                    # 判断双倍卡
                    if self.double_points_card_cnt > 0:
                        # 根据当前段位拿到胜利点数与失败点数
                        self.points_diff = int(self.points_diff * 2)
                        print(" 触发双倍卡 - 点数翻倍为: " + str(self.points_diff))
                        self.double_points_card_cnt = int(self.double_points_card_cnt - 1)

                    # 判断连胜
                    self.now_win_streak = int(self.now_win_streak + 1)
                    print(" 当前连胜 = " + str(self.now_win_streak))
                    # 根据连胜判断添加的额外点数
                    streak_extra_points = int(Tool_GetExtraPointsbyWinStreak(self.now_win_streak))
                    self.points_diff = int(self.points_diff + streak_extra_points)

                # 判断是否会再次触发晋级赛
                if  self.points_diff >= 100:
                    print("会【再】一次触发晋级赛")
                    print("now_rank_points = " + str(self.now_rank_points) + " points_diff = " + str(
                        self.points_diff) + " 胜利后点数会超100")
                    self.next_round_promotion = True
                    self.next_round_relegation = False
                    self.points_diff = 100
                    print("点数被强平为 points_diff = " + str(self.points_diff))

            else:
                # 否

                if self.function_lock:

                    # 判断双倍卡
                    if self.double_points_card_cnt > 0:
                        # 根据当前段位拿到胜利点数与失败点数
                        self.points_diff = int(self.points_diff * 2)
                        print(" 触发双倍卡 - 点数翻倍为: " + str(self.points_diff))
                        self.double_points_card_cnt = int(self.double_points_card_cnt - 1)

                    # 判断连胜
                    self.now_win_streak = int(self.now_win_streak + 1)
                    # 根据连胜判断添加的额外点数
                    streak_extra_points = int(Tool_GetExtraPointsbyWinStreak(self.now_win_streak))
                    self.points_diff = int(self.points_diff + streak_extra_points)

                # 判断是否会触发晋级赛
                if self.now_rank_points + self.points_diff >= 100:
                    print("会触发晋级赛")
                    print("now_rank_points = " + str(self.now_rank_points) + " points_diff = " + str(
                        self.points_diff) + " 胜利后点数会超100")
                    self.next_round_promotion = True
                    self.next_round_relegation = False
                    self.points_diff = int(100 - self.now_rank_points)
                    print("点数被强平为 points_diff = " + str(self.points_diff))

        # 失败
        else:
            self.next_round_promotion = False
            # 是否为保级赛
            if self.next_round_relegation:
                # 是
                self.next_round_relegation = False
                # 如果段位id = 1 且 掉分后为负值,则不掉段
                if self.now_rank == 1:
                    if self.now_points + self.points_diff < 0:
                        self.points_diff = -self.now_points
                        print("段位失分太多，强平为 " + str(self.points_diff))

                # 连胜清零
                self.now_win_streak = 0
                print("输掉比赛，连胜清零")

                if self.function_lock:
                    # 判断保护盾
                    if self.now_shield > 0:
                        self.points_diff = 0
                        self.now_shield = int(self.now_shield - 1)
                        print(" 触发保护盾 - 点数归为 : " + str(self.points_diff))
                        print("因此保护卡的存在又一次触发了保级赛")
                        self.next_round_relegation = True
                        self.next_round_promotion = False

                    # 判断buff
                    if self.buff_active:
                        self.points_diff = int(self.points_diff * (1 - self.now_points_protection_buff))
                        print("触发buff，点数归为：" + str(self.points_diff))

                # 判断是否因为保级卡的存在又一次触发了保级赛

            else:
                # 否
                # 如果段位id = 1 且 掉分后为负值,则不掉段
                if self.now_rank == 1:
                    if self.now_points + self.points_diff < 0:
                        self.points_diff = -self.now_points
                        print("段位失分太多，强平为 " + str(self.points_diff))

                # 连胜清零
                self.now_win_streak = 0
                print("输掉比赛，连胜清零")

                if self.function_lock:

                    # 判断保护盾
                    if self.now_shield > 0:
                        self.points_diff = 0
                        self.now_shield = int(self.now_shield - 1)
                        print(" 触发保护盾 - 点数归为 : " + str(self.points_diff))
                        if self.now_rank_points == 100:
                            # 特殊情况，在晋级赛时输掉比赛，有保护卡，则恢复晋级赛状态
                            self.next_round_promotion = True

                    # 判断buff
                    if self.buff_active:
                        self.points_diff = int(self.points_diff * (1 - self.now_points_protection_buff))
                        print("触发buff，点数归为：" + str(self.points_diff))

                # 判断是否触发了保级赛
                if self.now_rank_points + self.points_diff <= 0:
                    print("触发保级赛")
                    self.points_diff = - int(self.now_rank_points)
                    print("点数被强平为 = " + str(self.points_diff))
                    self.next_round_relegation = True
                    self.next_round_promotion = False

                    self.next_round_promotion = False

        ''' 刷新点数，刷新段位  '''
        # 总点数变化
        self.now_points = int(self.now_points + self.points_diff)

        print("最后总点数 = " + str(self.now_points))

        # 根据总点数刷新段位与now_rank_points
        now_rank = int(
            Tool_GetRankbyTotalPoints(self.now_points, self.next_round_promotion, self.next_round_relegation))

        if now_rank > self.now_rank:
            self.promotion_victory = True
            print(" (*^▽^*) 晋级成功 ， 从" + str(self.now_rank) + " 晋级到 " + str(now_rank))
        if now_rank < self.now_rank:
            self.relegation_victory = True
            print(" o(╥﹏╥)o 很可惜掉段了 ， 从" + str(self.now_rank) + " 掉到 " + str(now_rank))

        self.now_rank = now_rank
        # 刷新now_rank_points
        self.now_rank_points = int(Tool_GetNowRankPoints(self.now_points, self.now_rank))
        print("本局后段位为 " + str(self.now_rank) + " 当前点数为 " + str(self.now_rank_points))

        self.total_games_cnt = self.total_games_cnt + 1

        ''' 刷新所有任务 -  任务逻辑已经完成 '''

        print("当日此玩家活跃 = " + str(self.daily_games_cnt_dic[str(day_id)]))

        self.mission2_complete_condition = Tool_GetConditionbyRank2(self.now_rank)
        self.mission3_complete_condition = Tool_GetConditionbyRank3(self.now_rank)

        if self.mission2_status == False:
            if self.daily_games_cnt_dic[str(day_id)] >= self.mission2_complete_condition:
                self.mission2_status = True
                # 任务2收获奖励，获取双倍卡  or 段位保护卡
                reward_list = ["protect_card", "double_card"]
                reward = random.choice(reward_list)
                if reward == "protect_card":
                    self.now_shield = self.now_shield + 1
                    print("完成任务2： 获得段位保护卡一张 - 现在总数为：" + str(self.now_shield))
                    if self.now_shield > const_max_shield:
                        self.now_shield = const_max_shield
                        print(" 保护卡超上限，重置为： " + str(self.now_shield))
                else:
                    self.double_points_card_cnt = self.double_points_card_cnt + 1
                    print("完成任务2： 获得段位双倍卡一张 - 现在总数为：" + str(self.double_points_card_cnt))

        # 如果购买Pass，且任务3完成，激活Buff，否则buff消失
        if self.buy_pass:
            if self.mission3_status == False:
                if self.daily_games_cnt_dic[str(day_id)] >= self.mission3_complete_condition:
                    # 任务3收获奖励，获取buff
                    self.buff_active = True
                    self.mission3_status = True
                    print("完成任务3：激活buff")
        else:
            self.buff_active = False

        # 刷新状态
        # 状态判断与调整
        if self.daily_games_cnt_dic[str(day_id)] >= self.daily_active:
            self.player_status = "unactive"
        else:
            self.player_status = "matched"

    def GameMatch(self, day_id, matchPoolid, frame_id):
        '''
        :param day_id: 传入的day_id
        :param matchPoolid: 匹配到的matchPoolid
        :param frame_id: 传入的帧id
        :return: None
        返回胜负，更新self状态，通过matchPools 更新对应玩家状态
        '''

        bat_level_enemy = matchPools[int(matchPoolid) - 1].bat_level
        self_win = Tool_GetResultByBatLevel(self.bat_level, bat_level_enemy)

        self.GameSettlement(self_win, day_id, frame_id)

        enemy_win = False
        if self_win:
            enemy_win = False
        else:
            enemy_win = True
        print("****** enemy settlement ********")
        print(" 开始在匹配池 " + str(matchPoolid) + " 中随机玩家 ")

        num_can_match = Tool_GetPlayerCntfromStack(int(matchPoolid))
        print(" 这个匹配池中有 " + str(num_can_match) + " 个玩家")

        enemy_id = matchPools[int(matchPoolid) - 1].stack1_ready_match.getRandomReadyMatchPlayer()
        enemy_index_in_items = matchPools[int(matchPoolid) - 1].stack1_ready_match.getIndexByPlayerId(enemy_id)
        print("匹配到玩家 ：" + str(enemy_id) + " 该玩家在items中index = " + str(enemy_index_in_items))

        matchPools[int(matchPoolid) - 1].stack1_ready_match.items[enemy_index_in_items].GameSettlement(enemy_win,
                                                                                                       day_id, frame_id)


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
        return self.items[len(self.items) - 1]

    def size(self):
        '''返回栈的大小'''
        return len(self.items)

    def getRandomReadyMatchPlayer(self):
        list_cache = []
        for player in self.items:
            if player.player_status == "ready_match":
                list_cache.append(player.id)
        print("该匹配池中可选的玩家数量 = " + str(len(list_cache)))
        output_id_random = random.choice(list_cache)
        print("匹配到玩家" + str(output_id_random))
        return output_id_random

    def getIndexByPlayerId(self, player_id):
        index = 0
        for player in self.items:
            if player_id == player.id:
                return index
            index = index + 1

    def getSumReadyMatchPlayer(self):
        value = 0
        for player in self.items:
            if player.player_status == "ready_match":
                value = value + 1
        print(" 该匹配池中可匹玩家 = " + str(value))
        return value


# MatchPool
class MatchPool:
    '''
    匹配算法的基本数据结构
    '''
    id = 0
    bat_level = 1
    rank_id = 1
    matched_pools_list = []  # 存储对应rank_id 可匹配到的 MatchPool id
    matched_pools_probability = []  # 对应id下匹配到的概率

    # 堆栈
    stack1_ready_match = Stack()


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
            for column in range(column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row, column)).value)
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
            for column in range(column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row, column)).value)
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
            for column in range(column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row, column)).value)
            list_outside.append(list_inner)

        print("完成日活矩阵读取")
        for unit in list_outside:
            print(unit)

        return list_outside

    # 读取匹配池id矩阵
    def ReadMatchPoolIdMatrix(self):
        '''
        :return: 返回一个2维list， 存储匹配池id
        '''
        list_outside = []
        row_index_start = 88
        row_index_end = 117
        column_index_start = 4
        column_index_end = 11
        for row in range(row_index_start, row_index_end + 1):
            list_inner = []
            for column in range(column_index_start, column_index_end + 1):
                list_inner.append(ws.range((row, column)).value)
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
        output_win_list = []
        output_fail_list = []
        row_start = 5
        row_end = 34
        win_column = 18
        fail_column = 19

        for row in range(row_start, row_end + 1):
            output_win_list.append(ws.range((row, win_column)).value)
        for row in range(row_start, row_end + 1):
            output_fail_list.append(ws.range((row, fail_column)).value)

        print(" win_points_list = ")
        print(output_win_list)

        print(" fail_points_list = ")
        print(output_fail_list)

        return output_win_list, output_fail_list

    # 读取连胜数据
    def ReadWinStreakPoints(self):
        '''
        :return: 返回1个list, win_streak_list
        '''
        output_list = []
        start_row = 5
        end_row = 9
        column_index = 22

        for row in range(start_row, end_row + 1):
            output_list.append(ws.range((row, column_index)).value)
        print("win_streak_list =")
        print(output_list)

        return output_list

    # 读取任务数据
    def ReadMission2Condition(self):
        '''
        :return: 返回1个list, 任务2条件
        '''
        output_list = []
        row_index = 9
        start_column = 27
        end_column = 56
        for column in range(start_column, end_column + 1):
            output_list.append(ws.range((row_index, column)).value)
        print("Mission2 condition = ")
        print(output_list)

        return output_list

    def ReadMission3Condition(self):
        '''
        :return: 返回1个list, 任务3条件
        '''
        output_list = []
        row_index = 10
        start_column = 27
        end_column = 56
        for column in range(start_column, end_column + 1):
            output_list.append(ws.range((row_index, column)).value)
        print("Mission3 condition = ")
        print(output_list)

        return output_list

    def ReadSumPoints(self):
        '''
        :return: 返回总点数list
        '''
        output_list = []
        row_start = 5
        row_end = 34
        column_index = 17
        for row in range(row_start, row_end + 1):
            output_list.append(ws.range((row, column_index)).value)

        print(" rank_points_sum_list = ")
        print(output_list)

        return output_list


''' 主循环 
1.读取数据 
2.创建好匹配池，创建好玩家
3.根据天数进行匹配
4.返回指标

'''

fileReader1 = FileReader()
win_points_list, fail_points_list = fileReader1.ReadWinOrFailPoints()
win_streak_list = fileReader1.ReadWinStreakPoints()
rank_points_sum_list = fileReader1.ReadSumPoints()
WinRateMatrix_list = fileReader1.ReadWinRateMatrix()
Distribution_start_list = fileReader1.ReadDistributionMatrix()
DailyActive_list = fileReader1.ReadDailyActiveMatrix()
MatchPoolId_list = fileReader1.ReadMatchPoolIdMatrix()

Mission2Condition = fileReader1.ReadMission2Condition()
Mission3Condition = fileReader1.ReadMission3Condition()

# 创建匹配池
matchPools = []
rank_id_cache = 0
player_id = 1

for x in MatchPoolId_list:
    rank_id_cache = rank_id_cache + 1
    bat_level_cache = 0
    for y in x:
        bat_level_cache = bat_level_cache + 1
        matchPoolUnit = MatchPool()
        matchPoolUnit.stack1_ready_match = Stack()
        matchPoolUnit.bat_level = bat_level_cache
        matchPoolUnit.rank_id = rank_id_cache
        matchPoolUnit.id = int(y)

        # 可匹配到MatchPoolId
        matchPoolUnit.matched_pools_list, matchPoolUnit.matched_pools_probability = Tool_GetMatchPoolProbabilitybyId(
            matchPoolUnit.id)

        matchPools.append(matchPoolUnit)

        print("匹配池创建完成 " + " rank_id = " + str(matchPoolUnit.rank_id) + " bat_level = " + str(matchPoolUnit.bat_level))

print("matchPools 长度 = " + str(len(matchPools)))
for unit in matchPools:
    print(" ****** 匹配池id = " + str(unit.id) + " ******")
    print(" rank_id = " + str(unit.rank_id) + " bat_level = " + str(unit.bat_level))
    print("玩家数量 = " + str(len(unit.stack1_ready_match.items)))

###########################################################

# 创建一个玩家
rank_1 = 1
daily_active_1 = 7
bat_level_1 = 5
buy_pass = 1
days = 30



def Tool_GetMatchResultSingle(player):
    '''
    :param player: 传入的player对象
    :return: win or lose : 输出匹配的结果
    '''

    # 获取对应player下信息对应的 matchPoolId
    matchPoolId = int(MatchPoolId_list[player.now_rank - 1][player.bat_level - 1])

    # 获取能匹配到的id列表
    matched_pools_list = matchPools[matchPoolId - 1].matched_pools_list
    matched_pools_probability = matchPools[matchPoolId - 1].matched_pools_probability

    # 随机到特定的库
    matched_pool_id = Tool_GetRandomItemByWeight(matched_pools_list, matched_pools_probability)
    rank_id, bat_level = Tool_GetRankIdBatLvByMatchPoolId(matched_pool_id)

    print(" 匹配到一个 " + "rank_id = " + str(rank_id) + " bat_level = " + str(bat_level) + "的玩家")
    a_win = Tool_GetResultByBatLevel(player.bat_level, bat_level)
    if (a_win):
        print(" 结果赢了 ")
    else:
        print(" 结果输了 ")
    return a_win

days_points_con = []
for index in range(100):
    # 开启模式
    day_points = []
    player1 = Player(1, rank_1, daily_active_1, bat_level_1, buy_pass)

    # 时间控制 - 开始Play
    for day in range(days):
        print(" --------------------------")
        print(" 【【【【【【【【 第" + str(day) + " 天 】】】】】】】】")

        # 每天遍历所有玩家，执行匹配逻辑，并返回结果
        for frame in range(int(daily_active_1)):
            print(" ")
            print(" +++++++++++++++++++++ 第" + str(frame) + " 帧 +++++++++++++++++++++++++++++++ ")
            a_win = Tool_GetMatchResultSingle(player1)
            player1.GameSettlement(a_win, day, frame)
        day_points.append(player1.now_points)
    days_points_con.append(day_points)

days_points_sum = []
for x in range(30):
    days_points_sum.append(0)
for x in days_points_con:
    for h in range(len(x)):
        days_points_sum[h] =  days_points_sum[h] + x[h]

days_points_ave = []

for x in days_points_sum:
    ave= x/100
    days_points_ave.append(ave)



# 关闭模式
days_points_lock_con = []
for index in range(100):

    day_points_lock = []
    player2 = Player(2, rank_1, daily_active_1, bat_level_1, buy_pass= True)
    player2.function_lock = False
    days2= 30

    # 时间控制 - 开始Play
    for day in range(days2):
        print(" --------------------------")
        print(" 【【【【【【【【 第" + str(day) + " 天 】】】】】】】】")

        # 每天遍历所有玩家，执行匹配逻辑，并返回结果
        for frame in range(int(daily_active_1)):
            print(" ")
            print(" +++++++++++++++++++++ 第" + str(frame) + " 帧 +++++++++++++++++++++++++++++++ ")
            a_win = Tool_GetMatchResultSingle(player2)
            player2.GameSettlement(a_win, day, frame)

        day_points_lock.append(player2.now_points)
    days_points_lock_con.append(day_points_lock)

days_points_lock_sum = []
for x in range(30):
    days_points_lock_sum.append(0)
for x in days_points_lock_con:
    for h in range(len(x)):
        days_points_lock_sum[h] =  days_points_lock_sum[h] + x[h]

days_points_lock_ave = []
for x in days_points_lock_sum:
    ave= x/100
    days_points_lock_ave.append(ave)


# 更活跃模式
days_points_active_con = []
for index in range(100):
    day_points_more_active = []
    active_2 = daily_active_1 + 2
    # active_2 = daily_active_1
    player3 = Player(3, rank_1, active_2, bat_level= bat_level_1, buy_pass=True )
    days3= 30

    # 时间控制 - 开始Play
    for day in range(days3):
        print(" --------------------------")
        print(" 【【【【【【【【 第" + str(day) + " 天 】】】】】】】】")

        # 每天遍历所有玩家，执行匹配逻辑，并返回结果
        for frame in range(int(active_2)):
            print(" ")
            print(" +++++++++++++++++++++ 第" + str(frame) + " 帧 +++++++++++++++++++++++++++++++ ")
            a_win = Tool_GetMatchResultSingle(player3)
            player3.GameSettlement(a_win, day, frame)

        day_points_more_active.append(player3.now_points)
    days_points_active_con.append(day_points_more_active)


days_points_active_sum = []
for x in range(30):
    days_points_active_sum.append(0)
for x in days_points_active_con:
    for h in range(len(x)):
        days_points_active_sum[h] =  days_points_active_sum[h] + x[h]

days_points_active_ave = []

for x in days_points_active_sum:
    ave= x/100
    days_points_active_ave.append(ave)


import matplotlib.pyplot as plt
import numpy as np

ypoints = np.array(days_points_ave)
ypoints2 = np.array(days_points_lock_ave)
ypoints3 = np.array(days_points_active_ave)



plt.plot(ypoints, color = "g")
plt.plot(ypoints2, color = "r")
plt.plot(ypoints3, color = "b")


plt.show()