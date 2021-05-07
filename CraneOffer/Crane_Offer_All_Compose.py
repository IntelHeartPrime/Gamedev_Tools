# Crane Offer All Compose
# 递归算法枚举所有组合

# 3days的版本 18个整数和为680
# 5days的版本 27个整数和为1159

# return a list

def Crane_Offer_Get_Compose(value_left,sum,index,list_left,last_sum_lists):
    # 递归保存数据
    store_list =[]
    store_list.extend(list_left)
    store_list.append(value_left)

    # 递归求和
    sum_lists = 0
    sum_lists = sum_lists + last_sum_lists+value_left

    # 递归判断是否继续
    if_countine = True
    # if sum_lists >= 697:
        # if_countine = False

    index_def = index + 1

    if sum > 0 and value_left <100:
    #最大值的取值：maxvalue* indexs_last < sum

        if index <18:
            #print("--------------------- start --------------------")
            #print("sum = " + str(sum))

            sum_index_last = 18 - index_def
            min_value = value_left + 1
            # 求和所有想加
            sum_1_to_sum_indx_last_1 = 0

            if(sum_index_last >=1):
                for x in range(sum_index_last - 1):
                    sum_1_to_sum_indx_last_1 = sum_1_to_sum_indx_last_1 + x
                max_value = int((sum - sum_1_to_sum_indx_last_1) / sum_index_last)
            else:
                max_value = sum

            #print("sum_index_last = " + str(sum_index_last))

            # 最大值不可大于left_value的1.5倍

            if((max_value) > (value_left*1.5)):
                max_value = int(value_left*1.5)

            #打印 max_value
            #print("index = " + str(index) +"--min_value = "+ str(min_value)+ "--max_value = " +str(max_value))
            if (max_value > min_value):
                for x in range(min_value, max_value+1):
                    sum_x = sum - value_left
                    Crane_Offer_Get_Compose(x, sum_x, index_def, store_list,sum_lists)

                    # list_output = Crane_Offer_Get_Compose(x,sum_x,index_def)
                #print("-----------------------------")
            #else:
                #store_list.append(sum_lists)
                #print("warning!" + str(store_list))
                #print("-----------------------------")

        if index == 18:
            #store_list.append(sum_lists)
            sum_1 =0
            for x in store_list:
                sum_1 =sum_1+x
            store_list.append(sum_1)

            if sum_1 == 697:
                print(store_list)
            # store_list.append(1)
            #if(store_list[1] == 15):
            # print(store_list)

            '''
            
            sum_index_last = 18 - index
            index_def = index + 1
            min_value = value_left + 1
            max_value = int(value_left*1.5)
    
            if (max_value > min_value):
    
                # 判断和是否 = 697 若是，则返回，否则，返回空
                # 求出 sum
    
                for x in range(min_value, max_value):
                    if x+last_sum_lists == 697:
                        store_list.append(x)
                        print(store_list)
            '''
        return store_list


list_emtpy=[]
Crane_Offer_Get_Compose(10,697,1,list_emtpy,0)

# 需要加规则



