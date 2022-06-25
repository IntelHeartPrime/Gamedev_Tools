# 如何处理
# 遍历一层 - 标的列，获取标的列column 2~100
# 定位杆 - 根据第一行找值，有值者列存入list -{ 具体杆的lv}
# 函数 - 得出此行第一杆 元组[(id,lv),(id,lv)] &第二杆
# 生成Props
# 对sheet s5~s19分别做此

'''
输出格式；
"props": "[{\"balls\":[1],\"clubs\":[{\"id\":19,\"level\":5,\"w\":0.5},{\"id\":26,\"level\":2,\"w\":0.5}]}]",

x0 x1
[{"id":37,"l":4,"r":5},{"id":38,"l":4,"r":5}]
'''

# 下载文件


url_download = 'https://docs.google.com/spreadsheets/d/1KJAA-M-noxzXAQ3W5Vt0an_zELwsDiXL88iVAt49fFI/export?format=xlsx'
xlsx_file = requests.get(url_download)
open('MultipleStartPos.xlsx', 'wb').write(xlsx_file.content)


wb = xw.Book("MultipleStartPos.xlsx")

import json

# 支持输出中文

import os
work_dir = os.getcwd()
xlsx_dir = "CourseCardConfig.xlsx"

workbook_dir = os.path.join(work_dir, xlsx_dir)
print(workbook_dir)

json_file_name = "CourseCardConfig.json"

json_dir = os.path.join(work_dir, json_file_name)
print(json_dir)

# 工具

def clean_null(input_value):
    empty_value = ""
    if input_value == None:
        return empty_value
    return input_value


# 函数 - 输入（行数），输出某行第一杆与第二杆
def GetFirstClubsAndSecondClubs( row_index ):
    '''
    :param row_index: 行索引
    :return: [list,..]
    # 脚本转写非常重要
    # 周末多打几把游戏
    
    '''
    #
