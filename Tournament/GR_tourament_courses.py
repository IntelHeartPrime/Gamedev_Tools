# 输入 ：
# 18洞 or 9洞
# 安排的各个球场的1~6杆的人数与比例
# 不同档位奖励的切分比例值
# 球场安排的无序序列 / 某些位置固定球场，其他位置不定的无序序列

# 输出：
# 此安排下的各个档位的分数值
# 有利于收入的最佳安排

# 工具读取数据  csv文件


# Class TournamentDataUnit
# 属性：
# 1. course_id
# 2. par
# 3~8 rate1~rate6 （默认值为0）
# 应该由总数计算而来，存储 count1~count6
# 存储 count_all1 ~ count_all6
# birdie_up (birdie以上概率)
# eagle_up (eagle以上概率 ）
# albatross_up (albatross 以上概率 )
# hole_in_one (hole_in_one 概率 )
# improvement_room （提升空间指数/最佳发挥概率，par3 为 hole_in_one 概率 ，par4 为 hole_in_one 概率， par5 为 Albatross 概率 )
# good_level_rate （较好发挥概率，par3 为 hole_in_one 概率，par4 为 albatross概率，par5 为 Eagle 概率 ）
# simple_shot_rate （正常发挥概率，par3 为 Albatross_up , par4 为 Eagle_up , par5 为 Birdie_up ）
# difficulty(难度指数，improvment_room的倒数)
# ave_club(加权平均杆数）


# --------------------------------------------
import csv
import os

# 开始构造 类 TournamentDataUnit

class TournamentDataUnit(object):

    def __init__(self, course_id, par):
        self.course_id = course_id
        self.par = par
        self.rate = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        self.count = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        self.count_all = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]



        # 几大指标
        self.birdie_up = 0.00
        self.eagle_up = 0.00
        self.albatross_up = 0.00
        self.hole_in_one = 0.00

        #
        self.improvement_room = 0.00
        self.good_level_rate = 0.00
        self.simple_shot_rate = 0.00

        self.difficulty = 0.00

        self.ave_club=0.00

    # 增加累加
    def count_add(self, rate_index, count_single, count_all):
        self.count[rate_index-1] = self.count[rate_index-1]+count_single
        self.count_all[rate_index-1] = self.count_all[rate_index-1]+count_all



    # 得出所有指标
    def get_all_values(self):
        for i in range(0, 6):
            if self.count[i] == 0.00:
                self.rate[i] = 0.00
            else:
                self.rate[i]=self.count[i]/self.count_all[i]
        self.birdie_up = self.rate[0]+self.rate[1]+self.rate[2]+self.rate[3]
        self.eagle_up = self.rate[0]+self.rate[1]+self.rate[2]
        self.albatross_up = self.rate[0]+self.rate[1]
        self.hole_in_one = self.rate[0]

        if self.par == 3:
            self.improvement_room = self.hole_in_one
            self.good_level_rate = self.hole_in_one
            self.simple_shot_rate = self.albatross_up


        if self.par == 4:
            self.improvement_room = self.hole_in_one
            self.good_level_rate = self.albatross_up
            self.simple_shot_rate = self.eagle_up

        if self.par == 5:
            self.improvement_room = self.albatross_up
            self.good_level_rate = self.eagle_up
            self.simple_shot_rate = self.birdie_up
        if self.improvement_room!=0:
            self.difficulty = 1/self.improvement_room


        # 计算加权杆数
        for x in range(0,6):
            club = x+1
            self.ave_club = self.ave_club+club*self.rate[x]




# 开始读取Csv数据以遍历类并输出新的Csv
def read_csv_file_tournament_data_output(filename_read, filename_output):
    # OpenCsv
    # Create a List<string> of Course_id
    # Create a dictionary<course_id:string , TournamentDataUnit>
    # 遍历Csv，如有相应course_id 则，对字典内相应对象做处理
    # 否则创建新对象
    # 将所有数据写入新的Csv中

    course_list = []
    course_dict = dict()


    with open(filename_read) as f:
        f_csv = csv.reader(f)

        for row in f_csv:
            #print(row)
            # row 为 array or list
            # 判断字典Key值中是否有某一值
            if course_dict.__contains__(row[1]):
                course_dict[row[1]].count_add(int(row[5]), int(row[6]), int(row[7]))
            else:
                course_dict[row[1]] = TournamentDataUnit(row[1], int(row[3]))

            #print(len(course_dict))

        for key in course_dict.keys():
            course_dict[key].get_all_values()


        #写入操作
        header=["course", "Par", "Birdie_up", "Eagle_up", "Albatross_up", "hole_in_one", "improvement_room", "good_level_rate", "simple_shot_rate", "diffulty", "aveClub"]
        writer_final=[]
        with open(workfilepath+filename_output, 'w', newline='')as f:
            ff = csv.writer(f)

            ff.writerow(header)

            for value in course_dict.values():
                row_write = [str(value.course_id),str(value.par),str(value.birdie_up),str(value.eagle_up),str(value.albatross_up),str(value.hole_in_one),str(value.improvement_room),str(value.good_level_rate),str(value.simple_shot_rate),str(value.difficulty), str(value.ave_club)]
                print(row_write)
                writer_final.append(row_write)
            ff.writerows(writer_final)


workfilepath=os.getcwd();
print(workfilepath)

#read_csv_file_tournament_data_output("/Users/fotoable/PycharmProjects/GameIndustry /tournament_data.csv","")
read_csv_file_tournament_data_output(workfilepath+"/tournament_data.csv","/csvdir.csv")


# 思路
# 定义球场的可提升空间与难度指数
# improvement_room （提升空间指数/最佳发挥概率，par3 为 hole_in_one 概率 ，par4 为 hole_in_one 概率， par5 为 Albatross 概率 )
# Difficulty（难度指数，为提升空间的倒数）
# ave_club(加权杆数，球场的加权平均杆数）
# 对所有球场按照 Difficulty 排序分为三段，保证以下约束条件：
# 1. 9洞锦标赛 par3，par4，par5 各三个
# 2. 各锦标赛都均匀包含三段Difficulty的球场，保证不同等级的玩家都会有重刷球场的动力
# 3. 前两个9洞锦标赛的加权平均总杆数大致相等
# 4. 能区分出主题
