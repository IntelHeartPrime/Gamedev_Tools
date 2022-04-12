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

class Card():
    def __init__(self):
        self.id = 1
        self.level = 1
        self.max_star


class player():
    def __init__(self):

        ''' 挂机向属性 '''
        self.now_star = 0   # 当前星星数
        self.chest_coin_speed = 0.0     # 宝箱币获取速度 s
        self.upgrade_coin_speed = 0.0   # 升级币获取速度 s
        self.now_chest_coin = 0     # 当前chest_coin 存量
        self.now_upgrade_coin = 0   # 当前升级币存量

         ''' 球场卡进度 '''
        self.card_list = []     # 其中为card类


''' 数据读入&数据预存储 '''


