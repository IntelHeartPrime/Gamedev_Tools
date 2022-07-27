import shutil


src_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/CourseConfig.json"


src_path_to = r"/Users/yanxin/SingleMode/SinglePlayerForTest/Golf/misc/AIGnerate/Simulator/bin/Debug/Json/CourseConfig.json"



shutil.copy(src_path, src_path_to)

print(' Replaced courseconfig in singleMode ')

