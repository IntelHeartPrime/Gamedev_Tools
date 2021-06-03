
'''

要输出的json格式
{
        "course_id": 17300,
        "id": 17300,
        "props": [
            {
                "balls": [
                    1
                ],
                "clubs": [
                    {
                        "id": 31,
                        "level": 11
                    },
                    {
                        "id": 32,
                        "level": 11
                    }
                ]
            },
            {
                "balls": [
                    1
                ],
                "clubs": [
                    {
                        "id": 37,
                        "level": 6
                    },
                    {
                        "id": 38,
                        "level": 5
                    }
                ]
            },
            {
                "balls": [
                    1
                ],
                "clubs": [
                    {
                        "id": 37,
                        "level": 6
                    },
                    {
                        "id": 38,
                        "level": 6
                    }
                ]
            },
            {
                "balls": [
                    1
                ],
                "clubs": [
                    {
                        "id": 37,
                        "level": 5
                    },
                    {
                        "id": 38,
                        "level": 5
                    }
                ]
            },
            {
                "balls": [
                    1
                ],
                "clubs": [
                    {
                        "id": 31,
                        "level": 11
                    },
                    {
                        "id": 63,
                        "level": 5
                    }
                ]
            }
        ],
        "tour": 17
    },
'''

# props config 工具的写法：
# 母字典: courses_id:int ,id:int ,props(subdictionary):（balls: int or int_list , clubs(a list of dictionary): {id: int level: int}
# 逐行读取xlsx数据并且导出到json


from openpyxl import load_workbook
import json

wb = load_workbook("Props_config .xlsx")
ws = wb.active

# test the data frame

unit_dic = {}
unit_dic.update({"course_id": 10600})
unit_dic.update({"id": 10600})
props_list = []
props_dic = {"props": props_list}

unit_dic.update(props_dic)
unit_dic.update({"tour": 17})

props_list_unit = {}
props_list_unit.update({"balls": [1, 2]})
clubs_list = []
props_list_unit.update({"clubs": clubs_list})
clubs_list_unit1 = {"id": 26, "level": 4}
clubs_list_unit2 = {"id": 27, "level": 5}
clubs_list.append(clubs_list_unit1)
clubs_list.append(clubs_list_unit2)

props_list.append(props_list_unit)

# test output the json file

with open("Props_config.json", "w") as json_file:
    json_str = json.dumps(unit_dic, indent=4)
    json_file.write(json_str)

