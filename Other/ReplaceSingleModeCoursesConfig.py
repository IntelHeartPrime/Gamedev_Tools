import shutil


src_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/CourseConfig.json"


src_path_to = r"/Users/yanxin/SingleMode/SinglePlayerForTest/Golf/Assets/Resources/External/LocalData/CourseConfig.json"



shutil.copy(src_path, src_path_to)

print(' Replaced courseconfig in singleMode ')

