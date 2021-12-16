# How to simulate
# Output: log.csv ; Chart

# Tools

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

def Tool_GetIfTriggerByRankInfo( now_rank_points, points_diff):
    '''
    :param now_rank_points: 当前段位积分
    :param points_diff: 添加积分
    :return: bool True:触发 False: 不触发
    '''
    if now_rank_points + points_diff >=100:
        return True
    else:
        return False




# Player
class Player:
    #Attributes

    #初始信息
    id = 0
    origin_rank = 0
    bat_level = 1
    daily_active = 0
    buy_pass = False
    player_type = 1

    #段位&点数
    now_points = 0
    now_rank = 0
    now_rank_points = 0
    total_games = 0

    #卡*BUFF&连胜
    now_shield = 0
    double_points_card_cnt = 0

    now_win_streak = 0

    now_points_protection_buff = 0.0
    now_buff_time = 0.0

    # Mission
    mission1_now_points = 0
    mission2_now_points = 0
    mission3_now_points = 0

    mission1_complete_condition = 0
    mission2_complete_condition = 0
    mission3_complete_condition = 0

    mission1_status = False
    mission2_status = False
    mission3_status = False

    # Log
    points_log_list = []

    # Cache
    diff_points = 0 # 当前比赛缓存点数变化

    def __init__(self,  id, origin_rank, daily_active, bat_level, buy_pass):
        self.id = id
        self.origin_rank = origin_rank
        self.bat_level = bat_level
        self.daily_active = daily_active
        self.buy_pass = buy_pass

    def GameSettlement(self, result):
        '''

        :param result: bool 胜利/失败
        '''

        self.points_diff = Tool_GetPointsDiffbyRank(self.now_rank, result)

        # 胜利
        if result == True:

            # 判断双倍卡
            if self.double_points_card_cnt>0:
                # 根据当前段位拿到胜利点数与失败点数
                self.points_diff = self.points_diff*2
                print(" 触发双倍卡 - 点数翻倍为: " + str(self.points_diff))

            # 判断连胜
            self.now_win_streak = self.now_win_streak + 1
            # 根据连胜判断添加的额外点数
            streak_extra_points = Tool_GetPointsDiffbyRank(self.now_win_streak)
            self.points_diff = self.points_diff + streak_extra_points

            # 判断是否触发晋级赛
            promotion = Tool_GetIfTriggerByRankInfo(self.now_rank_points,self.points_diff)
            if (promotion):
                self.points_diff = tier_upgrade_score - self.now_points

        # 失败
        else:
            # 连胜清零
            self.now_win_streak = 0

            # 判断保护盾
            if self.now_shield > 0:
                self.points_diff = 0
                print(" 触发保护盾 - 点数归为 : " + str(self.points_diff))




# MatchManager
class MatchManager:
    id = 0

    def __init__(self):
        #根据段位+杆等级进行匹配
        #所有处于活跃状态的玩家
        #进行逐个匹配并更新状态
        #优化算法，每次不需要完全遍历
        #每完成一对匹配，直接输出比赛结果，更新所有状态
        #并打印所有信息
        self.id = 0

        '''
        匹配规则
        优先从同段位处匹配，匹不到则两端+1，再匹不到两端+2，... 直到+5 
        
        '''

class FileReader:
    '''
    从Excel中读取各类数据加载到 『数据容器』 中
    '''


