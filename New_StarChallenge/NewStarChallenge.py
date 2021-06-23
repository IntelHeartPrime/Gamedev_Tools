
import xlwings as xw

import json

wb = xw.Book("NewStarChallenge.xlsx")

ws = wb.sheets['Sheet1']

# 计算各类情况下所获得的星星

day_tickets = float(ws.range((22, 2)).value)

easy_star_times = float(ws.range((3,2)).value)
medium_star_times = float(ws.range((3,3)).value)
hard_star_times = float(ws.range((3,4)).value)
nightmare_star_times = float(ws.range((3,5)).value)

easy_lv_star = float(ws.range((13,2)).value)
medium_lv_star = float(ws.range((13,3)).value)
hard_lv_star = float(ws.range((13,4)).value)
nightmare_lv_star = float(ws.range((13,5)).value)

print("easy_lv_star = " + str(easy_lv_star) + " medium = " + str(medium_lv_star))
print("hard = " + str(hard_lv_star) + " nightmare = "+ str(nightmare_lv_star))

easy_lock_star = float(ws.range((2,2)).value)
medium_lock_star = float(ws.range((2,3)).value)
hard_lock_star = float(ws.range((2,4)).value)
nightmare_lock_star = float(ws.range((2,5)).value)


def getAllDaysStars():
    global ws
    # player_type 1 正常升级玩家
    # 2 恒定第一级玩家
    # 3 最高第二级玩家
    # 4 最高第三级玩家

    # 胜率 = 1 的玩家 

    times = [1, 1.5, 2]
    # 正常升级玩家 

    unlock_medium = 0
    unlock_hard = 0
    unlock_nightmare = 0

    all_days_star = 0.0
    now_rank = "easy"

    inter_flag = 0

    for t in range(len(times)):
        for x in range(1, 8):
            for y in range(int(day_tickets*times[t])):

                once_star_get = 0
                if now_rank == "easy":
                    once_star_get = easy_lv_star
                elif now_rank == "medium":
                    once_star_get = medium_lv_star
                elif now_rank == "hard":
                    inter_flag = inter_flag + 1
                    if inter_flag == 2:
                        once_star_get = hard_lv_star
                        inter_flag = 0
                elif now_rank == "nightmare":
                    inter_flag = inter_flag + 1
                    if inter_flag == 3:
                        once_star_get = nightmare_lv_star
                        inter_flag = 0

                if (all_days_star + once_star_get) >= easy_lock_star:
                    now_rank = "easy"
                if (all_days_star + once_star_get) >= medium_lock_star:
                    now_rank = "medium"
                    if unlock_medium == 0:
                        unlock_medium = x
                if (all_days_star + once_star_get) >= hard_lock_star:
                    now_rank = "hard"
                    if unlock_hard == 0:
                        unlock_hard = x
                if (all_days_star + once_star_get) >= nightmare_lock_star:
                    now_rank = "nightmare"
                    if unlock_nightmare == 0:
                        unlock_nightmare = x
                all_days_star = all_days_star + once_star_get
            print("today is " + str(x) + " all_star = " + str(all_days_star))
            ws.range((24+x, 2*(t+1))).value = all_days_star
            ws.range((25, 10)).value = unlock_medium
            ws.range((26, 10)).value = unlock_hard
            ws.range((27, 10)).value = unlock_nightmare

        all_days_star = 0

        # 恒定第一级玩家
        all_days_star = 0.0
        now_rank = "easy"

        for t in range(len(times)):
            for x in range(1, 8):
                for y in range(int(day_tickets * times[t])):
                    once_star_get = 0
                    if now_rank == "easy":
                        once_star_get = easy_lv_star
                    if (all_days_star + once_star_get) >= easy_lock_star:
                        now_rank = "easy"

                    all_days_star = all_days_star + once_star_get
                print("today is " + str(x) + " all_star = " + str(all_days_star))
                ws.range((33 + x, 2*(t+1))).value = all_days_star

            all_days_star = 0


    # 最高第二级玩家

    unlock_medium = 0

    all_days_star = 0.0
    now_rank = "easy"

    for t in range(len(times)):
        for x in range(1, 8):
            for y in range(int(day_tickets*times[t])):
                once_star_get = 0
                if now_rank == "easy":
                    once_star_get = easy_lv_star
                elif now_rank == "medium":
                    once_star_get = medium_lv_star

                if (all_days_star + once_star_get) >= easy_lock_star:
                    now_rank = "easy"
                if (all_days_star + once_star_get) >= medium_lock_star:
                    now_rank = "medium"
                    if unlock_medium == 0:
                        unlock_medium = x

                all_days_star = all_days_star + once_star_get
            print("today is " + str(x) + " all_star = " + str(all_days_star))
            ws.range((42+x, 2*(t+1))).value = all_days_star
            ws.range((43,10)).value = unlock_medium

        all_days_star = 0


        # 最高第三级玩家 

        unlock_medium = 0
        unlock_hard = 0

        all_days_star = 0.0
        now_rank = "easy"

        for t in range(len(times)):
            for x in range(1, 8):
                for y in range(int(day_tickets * times[t])):

                    once_star_get = 0
                    if now_rank == "easy":
                        once_star_get = easy_lv_star
                    elif now_rank == "medium":
                        once_star_get = medium_lv_star
                    elif now_rank == "hard":
                        inter_flag = inter_flag + 1
                        if inter_flag == 2:
                            once_star_get = hard_lv_star
                            inter_flag = 0


                    if (all_days_star + once_star_get) >= easy_lock_star:
                        now_rank = "easy"
                    if (all_days_star + once_star_get) >= medium_lock_star:
                        now_rank = "medium"
                        if unlock_medium == 0:
                            unlock_medium = x
                    if (all_days_star + once_star_get) >= hard_lock_star:
                        now_rank = "hard"
                        if unlock_hard == 0:
                            unlock_hard = x

                    all_days_star = all_days_star + once_star_get
                print("today is " + str(x) + " all_star = " + str(all_days_star))
                ws.range((51 + x, 2*(t+1))).value = all_days_star
                ws.range((52,10)).value = unlock_medium
                ws.range((53,10)).value = unlock_hard

                wb.save("NewStarChallenge.xlsx")
            all_days_star = 0


getAllDaysStars()


