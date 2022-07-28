import requests

def postContentToMyFlomo( string_input ):
    url = 'https://flomoapp.com/iwh/Mjk2Nw/b6cb16b6e45488200b16a6dd1b01ea21/'
    myobj = {'content': str(string_input)}

    x = requests.post(url, data=myobj)
    print("Post successful")
    print(x.text)



postContentToMyFlomo("专注是快乐的基础之一 #专注 #快乐")