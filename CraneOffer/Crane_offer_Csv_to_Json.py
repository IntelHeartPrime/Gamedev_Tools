import json
import csv

# 读取csv
# 将csv输出为json

# Csv配置格式 level, min, max, grade, prop_type, prop_id, prop_num, prop_color, chest_type
# 读取Csv后按照逐行写进Json中


csv_file_path = "csvCraneOfferRewards.csv"

# 字典List
json_dict_list = []


def readcsvtodict():
    with open(csv_file_path) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            # 将row中信息存入Object中
            new_dict = {
                "level": int(row[0]),
                "min": int(row[1]),
                "max": int(row[2]),
                "grade": int(row[3]),
                "reward": {
                    "prop_type": int(row[4]),
                    "prop_id": int(row[5]),
                    "prop_num": int(row[6]),
                    "prop_color": int(row[7]),
                    "chest_type": int(row[8])
                }
            }
            json_dict_list.append(new_dict)

# 对象进行实例化输出到Json

readcsvtodict()
with open("Crane_offer_tickets_rewards.json", "w") as json_file:
    index = 0
    for dict_unit in json_dict_list:
        index = index + 1
        json_str = json.dumps(dict_unit, indent=4)
        if( index < len(json_dict_list)):
            json_file.write(json_str + ",")
        else:
            json_file.write(json_str)
        json_file.write("\r")


