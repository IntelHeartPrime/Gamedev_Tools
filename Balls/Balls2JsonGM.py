import xlwings as xw
import json


wb = xw.Book("Balls.xlsx")
ws = wb.sheets['Sheet1']
json_dir = "allZeroWindBalls.json"

max_row_index = 400

list = []

for x in range(2,max_row_index):
    if ws.range((x,1)).value != None and ws.range((x,1)).value != "":
        if ws.range((x,18)).value != None and ws.range((x,18)).value !="":
            dic_unit = {}
            ball_id = int(ws.range((x,1)).value)
            dic_unit.update({"prop_id": ball_id})
            dic_unit.update({"prop_type": 0 })
            dic_unit.update({"prop_num": 100 })
            dic_unit.update({"prop_level": 0 })
            list.append(dic_unit)
            print(" add balls " + str(ball_id))

with open(json_dir, "w") as json_file:
    json_str = json.dumps(list, indent=4)
    json_file.write(json_str)


