import requests

def postContentToMyFlomo( string_input ):
    url = 'https://flomoapp.com/iwh/Mjk2Nw/b6cb16b6e45488200b16a6dd1b01ea21/'
    myobj = {'content': str(string_input)}

    x = requests.post(url, data=myobj)
    print("Post successful")
    print(x.text)



postContentToMyFlomo("- 管理的目的 - 1.成事 - 2.保持全面领先 #管理 #成事")