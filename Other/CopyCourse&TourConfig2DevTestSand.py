import shutil


src_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/CourseConfig.json"
dev_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/dev/CourseConfig.json"
sand_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/sandbox/CourseConfig.json"
test_path = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/test/CourseConfig.json"

src_path_tour = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/TourConfig.json"
dev_path_tour = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/dev/TourConfig.json"
sand_path_tour = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/sandbox/TourConfig.json"
test_path_tour = r"/Users/yanxin/GolfConfigOnly/GolfConfigOnly/test/TourConfig.json"


shutil.copy(src_path, dev_path)

print(' Course Copied 2 dev')

shutil.copy(src_path, sand_path)

print(' Course Copied 2 sandbox')

shutil.copy(src_path, test_path)

print(' Course Copied 2 test')

'''  tour '''

shutil.copy(src_path_tour, dev_path_tour)

print(' Tour Copied 2 dev')

shutil.copy(src_path_tour, sand_path_tour)

print(' Tour Copied 2 sandbox')

shutil.copy(src_path_tour, test_path_tour)

print(' Tour Copied 2 test')
