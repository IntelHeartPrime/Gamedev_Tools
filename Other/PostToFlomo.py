import requests

def postContentToMyFlomo( string_input ):
    url = 'https://flomoapp.com/iwh/Mjk2Nw/b6cb16b6e45488200b16a6dd1b01ea21/'
    myobj = {'content': str(string_input)}

    x = requests.post(url, data=myobj)
    print("Post successful")
    print(x.text)



postContentToMyFlomo("看数据不能只看平均的数据，根据平均数据使用2-8定律反推最活跃玩家数据，从而制定你的活动目标 #游戏/数值策划")