import copy
import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont

import sys, csv
import random

''' 参数配置 '''

# 低中高档区间
low_group_ranks = [6, 7, 8]
mid_group_ranks = [3, 4, 5]
high_group_ranks = [1, 2]

# 小火与概率  {小火配置序列需概率配置序列同长度}
fire1_list = [1,2,3,4,5,6,7,8]
probability_list = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08]

# 小火参数
money_rate = 0.01
refresh_rate = 0.01
refresh_add = 0.01
overturn_card_diam_rate = 0.002
overturn_add = 0.003

# 大火参数
once_fire2_add = 0.5
fire2_full = 1.0

#初始值
default_group = mid_group_ranks
fire1_origin = 0.0
fire2_origin = 0.0

# 钻石消耗配置
refresh_diamonds_list = range(100,200)
turn_diamonds_list = [100,200,300,400,500,600,700,800,900]

'''

4级奖励*1，3级奖励*2，2级奖励*3，1级奖励*3
传奇卡*1，钻石*1，紫卡*1，随机卡*1，球*2，金币*3

逻辑写死在代码中

'''


# 奖励配置地址
csv_file_path = "cardsRewards.csv"


''' 奖励单元类 '''
class RewardUnit():
    def __init__(self):
        self.rewardContent = ""   # text 奖励内容
        self.num = 0 # int 奖励数量
        self.weight = 0.0 # float 权重
        self.level = 1 # 稀有度
        self.value = 0.0 # 价值 -方便价值统计
        self.lock = False # 开关 是否能被随机到

    def print_self(self):
        print(self.rewardContent + "," + str(self.num) + "," + str(self.weight) + "," + str(self.level)+ "," + str(self.value) +"," + str(self.lock))


''' 用于随机组奖励的类 '''
class RewardRandom():
    def __init__(self, reward_type, reward_list):
        self.reward_type = reward_type   #string 格式
        self.reward_list = reward_list

        self.stored_list = self.copyStoredList(self.reward_list)

    # 可复制输入的数组
    def copyStoredList(self, input_list):
        cache_list = []
        for x in input_list:
            new_x = RewardUnit()
            new_x.rewardContent = copy.copy(x.rewardContent)
            new_x.num = copy.copy(x.num)
            new_x.weight = copy.copy(x.weight)
            new_x.level = copy.copy(x.level)
            new_x.value = copy.copy(x.value)
            new_x.lock = copy.copy(x.lock)
            cache_list.append(new_x)
        return cache_list

    def getRandomReward(self, lv):

        reward_list_cache = []
        weight_list = []
        for x in self.reward_list:
            if ((x.lock == False) and (x.level == lv)):
                weight_list.append(x.weight)
                reward_list_cache.append(x)
        #开始随机
        if(len(reward_list_cache)>0):
            random_result_list = random.choices(reward_list_cache, weights= weight_list, k=1)

            replace_list_cache = []
            for x in self.reward_list:
                if x == random_result_list[0]:
                    x.lock = True
                replace_list_cache.append(x)
            self.reward_list = replace_list_cache

            return random_result_list[0]
        else:
            raise Exception(str(self.reward_type)+"无可用奖励，请检查奖励配置", len(reward_list_cache))

    def printAllRewards(self):
        print(" Rewards config " + str(self.reward_type) + "START")
        for x in self.reward_list:
            x.print_self()
        print(" Rewards config " + str(self.reward_type) + "END")
        print()

    # 刷新所有奖励
    def refreshAllRewards(self):
        self.reward_list = self.copyStoredList(self.stored_list)

''' 读取奖励配置 '''
# RewardUnit 的 List
legendary_cards_rewards = []
epic_cards_rewards = []
rare_cards_rewards = []
common_cards_rewards = []
diamonds_rewards = []
ball_rewards = []
coin_rewards = []

# 读取csv，为以上List赋值
# csv格式要求为 rewardContent,num,weight,level,value,type
'''
只适用于策划数值规划

奖励对应关系：
club = 4  「其中 color不同: legen = 4 epic = 3 rare = 2 common = 1 」
定义：
legen = 44
epic = 43
rare = 42
common = 41

diamond = 2
ball = 5
coin = 3

'''
# 逐行读取，依据type将其分配到不同奖励List内

def readRewardConfigCsv():
    with open(csv_file_path) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            reward_unit = RewardUnit()
            reward_unit.rewardContent = row[0]
            reward_unit.num = float(row[1])
            reward_unit.weight = float(row[2])
            reward_unit.level = int(row[3])
            reward_unit.value = float(row[4])
            reward_unit.lock = False

            rewardType = int(row[5])
            if rewardType == 44:
                legendary_cards_rewards.append(reward_unit)
            if rewardType == 43:
                epic_cards_rewards.append(reward_unit)
            if rewardType == 42:
                rare_cards_rewards.append(reward_unit)
            if rewardType == 41:
                common_cards_rewards.append(reward_unit)
            if rewardType == 2:
                diamonds_rewards.append(reward_unit)
            if rewardType == 5:
                ball_rewards.append(reward_unit)
            if rewardType == 3:
                coin_rewards.append(reward_unit)


# 操作-读取配置
readRewardConfigCsv()

# 构建奖励类
lengen_rewards_class = RewardRandom("lengendary", legendary_cards_rewards)
lengen_rewards_class.printAllRewards()

epic_rewards_class = RewardRandom("epic", epic_cards_rewards)
epic_rewards_class.printAllRewards()

rare_rewards_class = RewardRandom("rare", rare_cards_rewards)
rare_rewards_class.printAllRewards()

common_rewards_class = RewardRandom("common", common_cards_rewards)
common_rewards_class.printAllRewards()

diamonds_rewards_class = RewardRandom("diamonds", diamonds_rewards)
diamonds_rewards_class.printAllRewards()

ball_rewards_class = RewardRandom("ball", ball_rewards)
ball_rewards_class.printAllRewards()

coin_rewards_class = RewardRandom("coin", coin_rewards)
coin_rewards_class.printAllRewards()


''' 读取/计算出所有奖励模式配置 '''
# 传奇卡的level==4，紫卡的level，随机卡的level，钻石的level==3，球1的level，球2的level，金币1的level，金币2的level，金币3的level
# 要求有1个level4，2个level3，3个level2，3个level1
# 为保证此模式的可行，需要保证紫卡配置至少需要 3*3条，橙卡白卡至少3*3条，球配置至少2*3条，金币配置至少3*3条
# 此处的右侧的3是指level一定要包含 lv1,lv2,lv3

available_composes = []

for legendary_lv in [4]:
    legen_unit = [legendary_lv, 4, 4]
    for diamond_lv in [3]:
        diamond_unit = [diamond_lv, 2, 0]
        for epic_lv in [1,2,3]:
            epic_unit = [epic_lv, 4, 3]
            for ball_lv1 in [1, 2, 3]:
                ball_unit1 = [ball_lv1, 5, 0]
                for ball_lv2 in [1, 2, 3]:
                    ball_unit2 = [ball_lv2, 5, 0]
                    for coin_lv1 in [1, 2, 3]:
                        coin_unit1 = [coin_lv1, 3, 0]
                        for coin_lv2 in [1, 2, 3]:
                            coin_unit2 = [coin_lv2, 3, 0]
                            for coin_lv3 in [1, 2, 3]:
                                coin_unit3 = [coin_lv3, 3, 0]
                                for otherCard_lv in [1, 2, 3]:
                                    for otherCard_color in [1,2,3]:
                                        otherCard_unit = [otherCard_lv, 4, otherCard_color]
                                        compose_mode = [legen_unit, diamond_unit, epic_unit, ball_unit1, ball_unit2, coin_unit1, coin_unit2, coin_unit3,otherCard_unit]
                                        # 判定该组合是否符合要求
                                        sum_4 = 0
                                        sum_3 = 0
                                        sum_2 = 0
                                        sum_1 = 0
                                        for x in compose_mode:
                                            if x[0] == 4:
                                                sum_4 = sum_4 + 1
                                            elif x[0] == 3:
                                                sum_3 = sum_3 + 1
                                            elif x[0] == 2:
                                                sum_2 = sum_2 + 1
                                            elif x[0] == 1:
                                                sum_1 = sum_1 + 1
                                        if ((sum_4 == 1) and (sum_3 == 2) and (sum_2 == 3) and (sum_1 == 3)):
                                            available_composes.append(compose_mode)


# 打印 available_composes
print(" all available compose： ")
for x in available_composes:
    print(x)
print("")


# 权重list
available_composes_weight = []
for x in range(len(available_composes)):
    available_composes_weight.append(10)


# 将available_compose 输出为可用格式： lv:rewardType, lv:rewardType, ....
'''
{
  "reward_conf": [
    [4,4,4],
    [3,7,3],
    [3,2,0],
    [3,4,3],
    [2,5,0],
    [2,3,0],
    [2,3,0],
    [1,3,0],
    [1,3,0]
  ],
  "weight": 10
}

  reward_conf 里的顺序  [稀有度, 奖品类型, 球杆类型（非球杆为0）]


'''


''' 逻辑部分 - 运行空间 '''

# 运行中的宏观参数
now_fire1_num = 0.0
now_probability_num = 0.0
now_fire2_num = 0.0
now_consumedDiamonds_num = 0.0
now_turnDiamonds_num = 0.0
now_refreshDiamonds_num = 0.0
now_rechargedMoney_num = 0.0

refresh_time = 0
turn_card_time = 0

now_legendary_location = 0  #奖励组的传奇卡位置


# 工具函数 - 根据 index 从list中取值，若index > count  则取最后一个值
def tool_getvalue(index, input_list):
    list_count = len(input_list)
    if index >= list_count:
        return input_list[list_count-1]
    else:
        return input_list[index]

# 工具函数 - 根据传入的值，输出其对应list的index
def tool_getlistindex(input_value, input_list):
    for x in range(len(input_list)):
        if input_value >= input_list[x]:
            return x
    # 找不到
    return None


# 随机函数 - 根据Fire1值随机出档位以及具体的Location
def randomRank_by_Fire(fire_value):
    # 根据fire_value 获取 Probability
    # 是否能随到中等档位
    # 是 -> 再随机中等档位Location return location_num
    # 否 -> return 0
    probability = 0.0

    probability_index = tool_getlistindex(fire_value, probability_list)
    if probability_index != None:
        probability = probability_list[probability_index]
    random_result = random.random()
    if random_result <= probability:
        # 随机到中等档位
        location = random.choice(mid_group_ranks)
        return location
    else:
        return 0

# 刷新所有奖励
def refresh_rewards():
    #全局变量声明

    global now_turnDiamonds_num
    global now_refreshDiamonds_num
    global now_rechargedMoney_num
    global refresh_time
    global turn_card_time

    # 更新消耗
    now_refreshDiamonds_num = now_refreshDiamonds_num + tool_getvalue(refresh_time, refresh_diamonds_list)
    refresh_time = refresh_time + 1



    ''' 
    # 实现步骤
    # 1.根据限制条件筛选组合库
    # 2.随机出组合模式「种类+稀有度」-无序
    # 3.随机出传奇卡
    # 4.按照模式随机出所有奖励
    '''
    # 根据限制条件筛选组合库


    # 根据权重获取配置模式
    random_compose_list = random.choices(available_composes, weights = available_composes_weight, k = 1)
    random_compose = random_compose_list[0]
    print("本次refresh组合id = " + str(refresh_time)+ "组合 = " + str(random_compose))

    # 随机出所有奖励

    output_rewards = []

    for x in random_compose:
        # 传奇卡
        if ((x[1] == 4) and (x[2] == 4)):
            reward_legen_card = lengen_rewards_class.getRandomReward(x[0])
            # print(reward_legen_card.rewardContent)
            output_rewards.append(reward_legen_card)
        # 钻石卡
        if (x[1] == 2):
            reward_diamond_card = diamonds_rewards_class.getRandomReward(x[0])
            # print(reward_diamond_card.rewardContent)
            output_rewards.append(reward_diamond_card)
        # 紫卡
        if ((x[1] == 4) and (x[2] == 3)):
            reward_epic_card = epic_rewards_class.getRandomReward(x[0])
            # print(reward_epic_card.rewardContent)
            output_rewards.append(reward_epic_card)
        # 橙卡
        if ((x[1] == 4) and (x[2] == 2)):
            reward_rare_card = rare_rewards_class.getRandomReward(x[0])
            # print(reward_rare_card.rewardContent)
            output_rewards.append(reward_rare_card)
        # 白卡
        if ((x[1] == 4) and (x[2] == 1)):
            reward_common_card = common_rewards_class.getRandomReward(x[0])
            # print(reward_common_card.rewardContent)
            output_rewards.append(reward_common_card)
        # 球
        if (x[1] == 5):
            reward_ball_card = ball_rewards_class.getRandomReward(x[0])
            # print(reward_ball_card.rewardContent)
            output_rewards.append(reward_ball_card)
        # 金币
        if (x[1] == 3):
            reward_coin_card = coin_rewards_class.getRandomReward(x[0])
            # print(reward_coin_card.rewardContent)
            output_rewards.append(reward_coin_card)

    # 输出本次奖励
    string_print = "本次获得组合奖励为 = "
    for x in output_rewards:
        string_print = string_print + " [" + str(x.rewardContent) + "] "
    print(string_print)

    lengen_rewards_class.refreshAllRewards()
    epic_rewards_class.refreshAllRewards()
    rare_rewards_class.refreshAllRewards()
    common_rewards_class.refreshAllRewards()
    diamonds_rewards_class.refreshAllRewards()
    ball_rewards_class.refreshAllRewards()
    coin_rewards_class.refreshAllRewards()

    return output_rewards

# test


result = refresh_rewards()


'''
确定奖励位置
'''

# 函数交换顺序
def listChangeValue( input_list, index1, index2):

    result =[]
    cache_value = input_list[index1]
    for x in input_list:
        result.append(x)
    result[index1] = result[index2]
    result[index2] = cache_value

    return result



def cardsSquence(output_rewards):


    global now_fire1_num
    global now_probability_num
    global now_fire2_num
    global now_consumedDiamonds_num
    global now_legendary_location

    # 确定传奇卡奖励位置
    # 大火判定
    if now_fire2_num < fire2_full:

        # 小火判定
        random_mid_location = randomRank_by_Fire(now_fire1_num)
        if random_mid_location != 0:
            # 小火随到中档
            now_legendary_location = random_mid_location
            # 小火值归零
            now_fire1_num = 0.0
        else:
            # 小火未随到中档，随小档
            now_legendary_location = random.choice(low_group_ranks)
        print("传奇卡位置 =" + str(now_legendary_location) + " | 卡顺序 = " + str(now_legendary_location+1))


    # 将其他奖励打乱
    # 将传奇杆奖励放在其应在的位置
    random.shuffle(output_rewards)

    index_cache = 0
    for x in range(len(output_rewards)):
        if output_rewards[x].level == 4:
            index_cache = x

    print( "index_cache =" + str(index_cache) )
    cards_squence = listChangeValue(output_rewards, index_cache, now_legendary_location)

    string_print = "本次奖励顺序为 = "
    for x in cards_squence:
        string_print = string_print + " [" + str(x.rewardContent) + "] "
    print(string_print)

    # 更新Fire值

    # 更新其他宏观参数

    # 刷新所有RewardsUnit lock值



    return cards_squence


#test
cardsSquence(result)



''' UI 部分 -  纯前端 + 交互 '''

class MyWindow(QMainWindow):
    # config my own window
    def __init__(self):

        ''' data '''
        self.fire1_num = now_fire1_num
        self.probability_num = now_probability_num
        self.fire2_num = now_fire2_num
        self.consumedDiamonds_num = now_consumedDiamonds_num
        self.turnDiamonds_num = now_turnDiamonds_num
        self.refreshDiamonds_num = now_refreshDiamonds_num
        self.rechargedMoney_num = now_rechargedMoney_num
        ''' data '''

        super(MyWindow, self).__init__()
        self.resize(720, 1280)
        # 居中
        self.center()

        self.setWindowTitle("Cards Activity")
        self.setWindowIcon(QIcon("cards.png"))
        self.initUI()


    def initUI(self):

        # Side Bar
        self.statusBar().showMessage('Simulation of Cards Activity')

        # Lable - Fire1 Value
        self.fire1_lab = QtWidgets.QLabel(self)
        self.fire1_lab.resize(300, 40)
        self.fire1_lab.setText("🔥FIRE1 = "+str((self.fire1_num)))
        self.fire1_lab.move(47, 30)
        self.fire1_lab.setFont(QFont("SansSerif", 20))

        # Lable - Probability Value
        self.probability_lab = QtWidgets.QLabel(self)
        self.probability_lab.resize(300, 40)
        self.probability_lab.setText("PROBABILITY = "+str((self.probability_num)))
        self.probability_lab.move(47, 110)
        self.probability_lab.setFont(QFont("SansSerif", 20))

        # Lable - Fire2 Value
        self.fire2_lab = QtWidgets.QLabel(self)
        self.fire2_lab.resize(300, 40)
        self.fire2_lab.setText("🔥FIRE2 = "+str((self.fire2_num)))
        self.fire2_lab.move(47, 70)
        self.fire2_lab.setFont(QFont("SansSerif", 20))

        # Lable - Comsumed Diamonds Number
        self.consumedDiamondsNum_lab = QtWidgets.QLabel(self)
        self.consumedDiamondsNum_lab.resize(300, 50)
        self.consumedDiamondsNum_lab.setText("CONSUMED 💎 = "+ str((self.consumedDiamonds_num)))
        self.consumedDiamondsNum_lab.move(426, 50)
        self.consumedDiamondsNum_lab.setFont(QFont("SansSerif", 20))

        # Lable - Recharged_money Number
        self.rechargeNum_lab = QtWidgets.QLabel(self)
        self.rechargeNum_lab.resize(300, 50)
        self.rechargeNum_lab.setText("RECHARGED 💰 = "+ str((self.rechargedMoney_num)))
        self.rechargeNum_lab.move(426, 80)
        self.rechargeNum_lab.setFont(QFont("SansSerif", 20))

        # Lable - turn diamonds
        self.turnDiamonds_lab = QtWidgets.QLabel(self)
        self.turnDiamonds_lab.resize(300, 50)
        self.turnDiamonds_lab.setText("TURN DIAMONDS: 💎 "+str((self.turnDiamonds_num)))
        self.turnDiamonds_lab.move(230, 720)
        self.turnDiamonds_lab.setFont(QFont("SansSerif", 20))

        # btn - Refresh
        self.refresh_btn = QtWidgets.QPushButton(self)
        self.refresh_btn.move(213,780)
        self.refresh_btn.resize(295,80)
        self.refresh_btn.setText("REFRESH 💎 " + str(self.refreshDiamonds_num))
        self.refresh_btn.clicked.connect(self.refreshBtnEvent)
        self.refresh_btn.setFont(QFont("SansSerif", 20))

        # btn - Reset
        self.reset_btn = QtWidgets.QPushButton(self)
        self.reset_btn.move(26,780)
        self.reset_btn.resize(91,72)
        self.reset_btn.setText("RESET")
        self.reset_btn.clicked.connect(self.resetBtnEvent)
        self.reset_btn.setFont(QFont("SansSerif", 20))

        # input_box [Recharge_money_num]
        self.recharge_input = QtWidgets.QLineEdit(self)
        self.recharge_input.move(600, 730)

        # btn - [Recharge]
        self.recharge_btn = QtWidgets.QPushButton(self)
        self.recharge_btn.move(600,780)
        self.recharge_btn.resize(91,72)
        self.recharge_btn.setText("Recharge")
        self.recharge_btn.clicked.connect(self.rechargeBtnEvent)
        self.recharge_btn.setFont(QFont("SansSerif", 15))

        ''' Cards Btns '''

        # 定义 Cards List
        self.cardsBtnsPos = []
        start_pos_x = 120
        start_pos_y = 180
        every_card_width = 150
        every_card_height = 160
        dis_x = 10
        dis_y = 10

        for x in range(3):
            for y in range(3):
                pos_x = start_pos_x + x*(every_card_width+dis_x)
                pos_y = start_pos_y + y*(every_card_height+dis_y)
                pos = [pos_x, pos_y]
                self.cardsBtnsPos.append(pos)

        # Card_btn1
        CardBtn1 = QtWidgets.QPushButton(self)
        CardBtn1.resize(every_card_width, every_card_height)
        CardBtn1.move(self.cardsBtnsPos[0][0], self.cardsBtnsPos[0][1])
        CardBtn1.setIcon(QIcon("cards.png"))
        CardBtn1.setText("1")
        CardBtn1.clicked.connect(self.cardEvent1)


        # Card_btn2
        CardBtn2 = QtWidgets.QPushButton(self)
        CardBtn2.resize(every_card_width, every_card_height)
        CardBtn2.move(self.cardsBtnsPos[1][0], self.cardsBtnsPos[1][1])
        CardBtn2.setIcon(QIcon("cards.png"))
        CardBtn2.setText("2")
        CardBtn2.clicked.connect(self.cardEvent2)

        # Card_btn3
        CardBtn3 = QtWidgets.QPushButton(self)
        CardBtn3.resize(every_card_width, every_card_height)
        CardBtn3.move(self.cardsBtnsPos[2][0], self.cardsBtnsPos[2][1])
        CardBtn3.setIcon(QIcon("cards.png"))
        CardBtn3.setText("3")
        CardBtn3.clicked.connect(self.cardEvent3)

        # Card_btn4
        CardBtn4 = QtWidgets.QPushButton(self)
        CardBtn4.resize(every_card_width, every_card_height)
        CardBtn4.move(self.cardsBtnsPos[3][0], self.cardsBtnsPos[3][1])
        CardBtn4.setIcon(QIcon("cards.png"))
        CardBtn4.setText("4")
        CardBtn4.clicked.connect(self.cardEvent4)

        # Card_btn5
        CardBtn5 = QtWidgets.QPushButton(self)
        CardBtn5.resize(every_card_width, every_card_height)
        CardBtn5.move(self.cardsBtnsPos[4][0], self.cardsBtnsPos[4][1])
        CardBtn5.setIcon(QIcon("cards.png"))
        CardBtn5.setText("5")
        CardBtn5.clicked.connect(self.cardEvent5)

        # Card_btn6
        CardBtn6 = QtWidgets.QPushButton(self)
        CardBtn6.resize(every_card_width, every_card_height)
        CardBtn6.move(self.cardsBtnsPos[5][0], self.cardsBtnsPos[5][1])
        CardBtn6.setIcon(QIcon("cards.png"))
        CardBtn6.setText("6")
        CardBtn6.clicked.connect(self.cardEvent6)

        # Card_btn7
        CardBtn7 = QtWidgets.QPushButton(self)
        CardBtn7.resize(every_card_width, every_card_height)
        CardBtn7.move(self.cardsBtnsPos[6][0], self.cardsBtnsPos[6][1])
        CardBtn7.setIcon(QIcon("cards.png"))
        CardBtn7.setText("7")
        CardBtn7.clicked.connect(self.cardEvent7)

        # Card_btn8
        CardBtn8 = QtWidgets.QPushButton(self)
        CardBtn8.resize(every_card_width, every_card_height)
        CardBtn8.move(self.cardsBtnsPos[7][0], self.cardsBtnsPos[7][1])
        CardBtn8.setIcon(QIcon("cards.png"))
        CardBtn8.setText("8")
        CardBtn8.clicked.connect(self.cardEvent8)

        # Card_btn9
        CardBtn9 = QtWidgets.QPushButton(self)
        CardBtn9.resize(every_card_width, every_card_height)
        CardBtn9.move(self.cardsBtnsPos[8][0], self.cardsBtnsPos[8][1])
        CardBtn9.setIcon(QIcon("cards.png"))
        CardBtn9.setText("9")
        CardBtn9.clicked.connect(self.cardEvent9)

        ''' Cards Btns '''

    # 为所有btn 添加 log
    def refreshBtnEvent(self):
        print("刷新一次")
        cards_group = refresh_rewards()
        cardsSquence(cards_group)

    def resetBtnEvent(self):
        print("")

    def rechargeBtnEvent(self):
        print(self.recharge_input.text())

    def cardEvent1(self):
        print("1")

    def cardEvent2(self):
        print("2")

    def cardEvent3(self):
        print("3")

    def cardEvent4(self):
        print("4")

    def cardEvent5(self):
        print("5")

    def cardEvent6(self):
        print("6")

    def cardEvent7(self):
        print("7")

    def cardEvent8(self):
        print("8")

    def cardEvent9(self):
        print("9")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def refreshAlldata_show(self):
        # 更新所有前端数值
        # 在按钮点击后刷新
        print("刷新所有前端显示")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec())

window()

