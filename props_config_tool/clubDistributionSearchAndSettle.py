'''逐行解析csv，并把数据统计于Excel中'''
'''
先搜索csv，获取course_id
根据course_id搜索Excel，定位该场景的行数区间
如果course_id 不变，则对该行数区间内进行遍历，若单个杆或者组合符合，则对该杆进行+1 
" 如果csv中杆等级不足，亦然+1 "  --- 需设置一此开关 
" 若对于某一组合而言，csv中等级都低于其，则也对此组合+1 ，也需设置开关 " 
'''

'''
数据结构

缓存区 
不同杆的样本数量
例如： { "37" : num } ... 
[[id,num],[row_index, column_index]] 
[id,num] 代表杆的id和数量
[row_index, column_index] 代表存储结果的位置的 row索引与column索引

在更换course_id 后清零

组合
例如： [ [ a, b] , [ c, d] ,[final_value_row, final_value_column],[cnt,0]]  
[a,b] 代表第一杆的 club_id & club_level
[c,d] 代表第二杆的 club_id & club_level

[final_value_row, final_value_column] 代表存储其结果的位置的 row索引与column索引  - Excel中
[cnt,0] 代表应该填入的值 

是否需要唯一标识

'''