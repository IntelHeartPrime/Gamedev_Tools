'''
对于不同类型的玩家进行模拟，从而得出相应结果

# 1.数据加载模块，加载各类预定数值
# 2.模拟模块
# 3.输出模块，输出各类图&指标，从而指导设计

'''

'''
配合 jupyternoteebook进行设计
'''

'''
思路
定义玩家行为:
1.有能开的宝箱，则根据偏好直接开对应宝箱
2.有能买的礼包，则根据预算与行为习惯可购买   付费习惯：固定预算 / 按需付费； 付费偏好： 日礼包向 / 周礼包向   是否会直接花钻石开宝箱
3.遇到杆等级不足的情况，则中断
4.按照每天的体力预算进行的玩家 （体力打没且超过预算为止） / 每日固定局数 
模拟一个玩家进行pve的全流程并记录所有变化
'''

'''
类 - 
1. Player类 玩家属性 & 记录
2. Card类 球场卡
'''

class Card_level():
    def __init__(self):
        ''' 关卡&卡片属性'''
        self.name = "" # 卡牌名字
        self.id = 1 # id
        self.level = 1 # 等级

        self.chapter_id = 1 # chapter_id
        self.chapter_index = 0 # chapter_index 一般为0，支线则顺序+
        self.side_story = False # 是否是支线
        self.region_tee = 1 # 大区id，也就是开球点id （1~ 4）

        self.par_star = 0
        self.birde_star = 0
        self.eagle_star = 0
        self.albatross_star = 0
        self.max_star = 0

        self.ave_star_ave_upgarde_coin = 0 # 平均每个星星所所能带来的升级币数量
        self.ave_star_out_reward_diamond = 0 # 平均每个星星所代表的局外奖励价值 - 钻石计价

        ''' 关卡&关卡现状 '''
        self.now_star = 0
        self.unlock = False # 关卡是否还未激活，无论何种原因
        self.full_star = False # 关卡是否满星

    def print_info(self):
        print("")
        print("-------------------------------")
        print("chapter_id = " + str(self.chapter_id))
        print("chapter_index = " + str(self.chapter_index))
        print("region_tee = " + str(self.region_tee))
        print("side_story = " + str(self.side_story))

        print("")
        print("card_name = " + str(self.name))
        print("card_id = " + str(self.id))
        print("card_level = " + str(self.level))

        print("")
        print("par_star = " + str(self.par_star))
        print("birde_star = " + str(self.birde_star))
        print("eagle_star = " + str(self.eagle_star))
        print("albatross_star = " + str(self.albatross_star))
        print("max_star = " + str(self.max_star))

        print("")
        print("ave_star_upgrade_coin = " + str(self.ave_star_ave_upgarde_coin))
        print("ave_star_out_reward_diamond = " + str(self.ave_star_out_reward_diamond))

        print("")
        print("now_star = " + str(self.now_star))
        print("unlock = " + str(self.unlock))
        print("full_star = " + str(self.full_star))




class player():
    def __init__(self):

        ''' 挂机向属性 '''
        self.now_star = 0   # 当前星星数
        self.chest_coin_speed = 0.0     # 宝箱币获取速度 s
        self.upgrade_coin_speed = 0.0   # 升级币获取速度 s

        self.now_chest_coin = 0     # 当前chest_coin 存量
        self.now_upgrade_coin = 0   # 当前升级币存量

        self.card_package = {} # { cardname: level }


    # 初始化card_package
    def initialCardList(self):
        # 读取数据，初始化card_package
        global card_name_id
        for x in card_name_id.keys():
            self.card_package.update({str(x): 0})

        print("")
        print("球场卡包初始化成功")
        print(self.card_package)


''' 我的代码写的像诗 '''


import xlwings as xw

wb = xw.Book("SimulatorRead.xlsx")
ws_gameMatrix = wb.sheets['gameMatrix']
ws_levelMatrix = wb.sheets['levelMatrix']
ws_dungeon = wb.sheets['dungeon']


''' Global'''

auto_refill_ticket = 8 # 自动恢复体力的最大量
tick_min = 5 # 一个tick所持续的分钟数


''' Global data container '''
card_name_id = {}  # 球场卡名字：id 的字典
main_level_list = [] # 主线关卡 card_level类的list
side_level_list = [] # 支线关卡 { level_index( "8-1") : card_level }


''' 
Global Function

Function Read Data -> Global data container
Read Data function 与 data container 一一对应
'''
def Read_card_name_id():
    global  card_name_id

    row_start = 40
    row_end = 47

    column_name = 1
    column_id = 2

    for row in range(row_start, row_end + 1):
        card_name = ws_levelMatrix.range((row, column_name)).value
        card_id = int(ws_levelMatrix.range((row, column_id)).value)

        card_name_id.update({str(card_name): card_id})

    print("")
    print("card_name_id 读取完毕")
    print(card_name_id)



def Read_levels():
    global card_name_id
    global main_level_list
    global side_level_list

    # 读取主线关卡信息

    print("开始读取主线")
    print("")

    row_start = 4
    while ws_dungeon.range((row_start, 2)).value != None:
        card1 = Card_level()
        card1.name = str(ws_dungeon.range((row_start, 2)).value)

        # 根据名字找id
        if len(card_name_id.keys()) > 1:
            for x in card_name_id.keys():
                if x == card1.name:
                    card1.id = card_name_id[x]

        card1.name = ws_dungeon.range((row_start, 3)).value
        card1.level = int(ws_dungeon.range((row_start, 4)).value)
        card1.chapter_id = int(ws_dungeon.range((row_start, 2)).value)
        card1.par_star = int(ws_dungeon.range((row_start, 6)).value)
        card1.birde_star = int(ws_dungeon.range((row_start, 7)).value)
        card1.eagle_star = int(ws_dungeon.range((row_start, 8)).value)
        card1.albatross_star = int(ws_dungeon.range((row_start, 9)).value)
        card1.max_star = int(ws_dungeon.range((row_start, 10)).value)

        card1.region_tee = int(ws_dungeon.range((row_start, 1)).value)

        card1.ave_star_ave_upgarde_coin = int(ws_dungeon.range((row_start, 11)).value)
        card1.ave_star_out_reward_diamond = int(ws_dungeon.range((row_start, 12)).value)

        card1.print_info()

        main_level_list.append(card1)

        row_start = row_start + 1

    print("主线读取完毕✔️")

    # 读取支线关卡信息
    print("")
    print("开始读取支线")
    row_start = 4
    row_end = 63
    for row in range(row_start, row_end + 1):
        if ws_dungeon.range((row, 14)).value != None:

            card1 = Card_level()
            card1.name = str(ws_dungeon.range((row_start, 2)).value)

            # 根据名字找id
            if len(card_name_id.keys()) > 1:
                for x in card_name_id.keys():
                    if x == card1.name:
                        card1.id = card_name_id[x]

            card1.name = ws_dungeon.range((row_start, 14)).value
            card1.level = int(ws_dungeon.range((row_start, 15)).value)
            card1.chapter_id = int(str(ws_dungeon.range((row_start, 16)).value).split("-")[0])
            card1.chapter_index = int(str(ws_dungeon.range((row_start, 16)).value).split("-")[1])
            card1.side_story = True

            card1.par_star = int(ws_dungeon.range((row_start, 17)).value)
            card1.birde_star = int(ws_dungeon.range((row_start, 18)).value)
            card1.eagle_star = int(ws_dungeon.range((row_start, 19)).value)
            card1.albatross_star = int(ws_dungeon.range((row_start, 20)).value)
            card1.max_star = int(ws_dungeon.range((row_start, 21)).value)

            card1.region_tee = int(ws_dungeon.range((row_start, 1)).value)

            card1.ave_star_ave_upgarde_coin = int(ws_dungeon.range((row_start, 22)).value)
            card1.ave_star_out_reward_diamond = int(ws_dungeon.range((row_start, 23)).value)

            card1.print_info()

            level_index = ws_dungeon.range((row_start, 16)).value
            side_story_dic = {}
            side_story_dic.update({str(level_index): card1})
            


''' PVE '''
def PVE():
    # 初始化pve数据 ，读取pve关卡，按照tick进行处理
    # 读取关卡分布
    print("")



''' test '''
Read_card_name_id()
player1 = player()
player1.initialCardList()
Read_levels()