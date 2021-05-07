# Analysis Arena Data
# Draw points Graphic

import numpy
import pandas
import matplotlib

def GetFinalImg(course_id,unit_length,total_length,file_name):

    arenaDataFil = pandas.read_csv(file_name)
    # steps
    # 按照course id 绘制
    # 输入 course id ，区间粒度 ，区间总量， 绘制出直方图即可

    arenaDataFil.columns = ['course_id','yards_from_pin','into_hole']
    arenaDataArray = numpy.array(arenaDataFil)

    print(arenaDataArray[0][1])
    # 遍历DataArray
    # 判断是否为course id
    # 是 遍历比较其距离球洞位置
    # 相应标识或者数组位置 +1
    # 将数组输出为直方图
    # 直方图y轴：数量 直方图横轴：距离粒度
    int int_count
    int_count=total_length/unit_length
    int[] range_array

    # start here to continue
    #for x in range(1:int_count):
        #


    for unit in arenaDataArray:
            if unit[0]==course_id:
                    print(unit)


GetFinalImg(14900,1,10,"21008.csv")



