import OEFUFP
import numpy
import time
# 动态构建BSW列表，BSW的个数是事先固定好的
BSW = globals()
for m in range(1, 4):
    BSW[str(m)] = []
num = 0
with open(r'C:\Users\Administrator\Desktop\data\T10I4D100K.txt') as database:
    for line in database:
        num += 1
        if num in range(1, 301):
            BSW[str(1)].append(line.split())
        elif num in range(301,5101):
            BSW[str(2)].append(line.split())
        elif num in range(5101,15001):
            BSW[str(3)].append(line.split())
        else:
            break
    print('数据的大小为：', num)
n = 15000  # 滑动窗口的大小
m1 = 300   # 滑动窗口1的大小
m2 = 4800  # 滑动窗口2的大小
m3 = 9900   # 滑动窗口3的大小
if __name__ == '__main__':
    print('开始执行')
    time_start = time.perf_counter()
    min_sup = 0.01
    # 每个BSW分别调用FIU找到频繁项集
    FI = globals()
    for m in range(1, 4):
        if m == 1:
            frequent_itemsets = OEFUFP.find_frequent_items(BSW[str(m)], 300, include_support=True)
        elif m == 2:
            frequent_itemsets = OEFUFP.find_frequent_items(BSW[str(m)], 4800, include_support=True)
        else:
            frequent_itemsets = OEFUFP.find_frequent_items(BSW[str(m)], 9900, include_support=True)
        # print('调用完成')
        FI[str(m)] = {}
        for itemset, support in frequent_itemsets:  # 将generator结果存入list
            if len(itemset) != 1:
                FI[str(m)][tuple(itemset)] = support
        # print('存放完成')
        # if m == 1:
        #     print('执行了1')
        # if m == 2:
        #     print('执行了2',)
        # if m == 3:
        #      print('执行了3')
        # result = sorted(FI[str(m)], key=lambda support: support[1])
    # 计算BSW之间的相似度,构建矩阵(矩阵元素都为1)并将相似度添加进去
    M = numpy.ones(shape=(4, 4))
    try:
        s12 = abs(len(FI['1'].keys() & FI['2'].keys())) / abs(len(FI['1'].keys() | FI['2'].keys()))
        s13 = abs(len(FI['1'].keys() & FI['3'].keys())) / abs(len(FI['1'].keys() | FI['3'].keys()))
        s23 = abs(len(FI['2'].keys() & FI['3'].keys())) / abs(len(FI['2'].keys() | FI['3'].keys()))
        # s12 = (len(FI['1'].keys() & FI['2'].keys()) / len(FI['2'].keys())) \
        #       + (len(FI['1'].keys() & FI['2'].keys()) / len(FI['1'].keys())) - 1
        # s13 = (len(FI['1'].keys() & FI['3'].keys()) / len(FI['3'].keys())) \
        #       + (len(FI['1'].keys() & FI['3'].keys()) / len(FI['1'].keys())) - 1
        # s23 = (len(FI['2'].keys() & FI['3'].keys()) / len(FI['2'].keys())) \
        #       + (len(FI['2'].keys() & FI['3'].keys()) / len(FI['3'].keys())) - 1
        M[0, 1] = s12
        M[1, 0] = s12
        M[0, 2] = s13
        M[2, 0] = s13
        M[1, 2] = s23
        M[2, 1] = s23
    except ZeroDivisionError:
        print("You can't divide by 0.")
    # print(M)
    # 定义存储结构，将候选项集的信息（FI的并集）存放在字典嵌套列表中
    # 将对应的频繁项集的计数添加到对应的字典列表中
    con_info = {}
    all_FI = {}
    for set in FI['1'].keys() | FI['2'].keys() | FI['3'].keys():
        con_info[set] = [0, 0, 0, 0]
        if set in FI['1']:
            con_info[set][0] = FI['1'][set]
        if set in FI['2']:
            con_info[set][1] = FI['2'][set]
        if set in FI['3']:
            con_info[set][2] = FI['3'][set]
    # 估计con_info中值为0的项集
    for keys in con_info:
        flag = 0
        flag1 = 0
        for i in range(0, 3):
            if con_info[keys][i] == 0:
                if i == 0:
                    flag = 1
                    sup = 1/2 * (round(M[0, 1] * con_info[keys][1], 4) + round(M[0, 2] * con_info[keys][2], 4))
                    # print('1的估值', sup)
                    if sup >= min_sup * m1:
                        sup1 = int(min_sup * m1)
                    else:
                        sup1 = sup
                elif i == 1:
                    flag1 = 1
                    if flag == 0:
                        sup = 1/2 * (round(M[0, 1] * con_info[keys][0], 4) + round(M[1, 2] * con_info[keys][2], 4))
                    else:
                        sup = round(M[1, 2] * con_info[keys][2], 4)
                        # print('2的估值', sup)
                    if sup >=min_sup * m2:
                        sup1 = int(min_sup * m2)
                    else:
                        sup1 = sup
                else:
                    if flag == 0 & flag1 == 0:
                        sup = 1/2 * (round(M[0, 2] * con_info[keys][0], 4) + round(M[1, 2] * con_info[keys][1], 4))
                    elif flag == 1 & flag1 == 0:
                        sup = round(M[1, 2] * con_info[keys][1], 4)
                    elif flag == 0 & flag1 == 1:
                        sup = round(M[0, 2] * con_info[keys][0], 4)
                    # print('3的估值', sup)
                    if sup >= min_sup * m3:
                        sup1 = int(min_sup * m3)
                        # print(sup1)
                    else:
                        sup1 = sup
                con_info[keys][i] = sup1
        #打印所有候选项集,以便计算支持度估计误差
        # print(keys,':',con_info[keys][0] + con_info[keys][1] + con_info[keys][2])
        # 根据阈值找出频繁项集
        if con_info[keys][0] + con_info[keys][1] + con_info[keys][2] >= min_sup * n:
            all_FI[keys] = con_info[keys][0] + con_info[keys][1] + con_info[keys][2]
    time_end = time.perf_counter()
    print('原始数据库挖掘的个数为：', len(all_FI))
    print('原始数据库的挖掘时间为：', time_end - time_start, 's')
    # print(all_FI)
# 处理新增数据库
time_end1 =time.perf_counter()
final_FI = {}
BSW[str(4)] = []
num1 = 0
with open(r'C:\Users\Administrator\Desktop\data\NT10I4D100K.txt') as newdatabase:
    for line in newdatabase:
        num1 += 1
        if num1 in range(1, 10001):
            BSW[str(4)].append(line.split())
        else:
            break
m = 4
n1 =10000
frequent_itemsets = OEFUFP.find_frequent_items(BSW[str(m)], 10000, include_support=True)
FI[str(m)] = {}
for itemset, support in frequent_itemsets:  # 将generator结果存入list
    if len(itemset) != 1:
        FI[str(m)][tuple(itemset)] = support
try:
    s14 = abs(len(FI['1'].keys() & FI['4'].keys())) / abs(len(FI['1'].keys() | FI['4'].keys()))
    s24 = abs(len(FI['2'].keys() & FI['4'].keys())) / abs(len(FI['2'].keys() | FI['4'].keys()))
    s34 = abs(len(FI['3'].keys() & FI['4'].keys())) / abs(len(FI['3'].keys() | FI['4'].keys()))
    # s14 = (len(FI['1'].keys() & FI['4'].keys()) / len(FI['4'].keys())) \
    #       + (len(FI['1'].keys() & FI['4'].keys()) / len(FI['1'].keys())) - 1
    # s24 = (len(FI['2'].keys() & FI['4'].keys()) / len(FI['4'].keys())) \
    #       + (len(FI['2'].keys() & FI['4'].keys()) / len(FI['2'].keys())) - 1
    # s34 = (len(FI['3'].keys() & FI['4'].keys()) / len(FI['4'].keys())) \
    #       + (len(FI['3'].keys() & FI['4'].keys()) / len(FI['3'].keys())) - 1
    M[0, 3] = s14
    M[3, 0] = s14
    M[1, 3] = s24
    M[3, 1] = s24
    M[2, 3] = s34
    M[3, 2] = s34
    # print(M)
except:
    print("You can't divide by 0.")
# print(M)
# 原不频繁现频繁和原频繁现频繁
for key1 in FI['4']:
    if not key1 in con_info:
        con_info[key1] = [0, 0, 0, FI['4'][key1]]
        sup1 = round(M[0, 3] * con_info[key1][3])
        if sup1 >= min_sup * m1:
            count = int(min_sup * m1)
        else:
            count = sup1
        sup2 = round(M[1, 3] * con_info[key1][3])
        if sup2 >= min_sup * m2:
            count1 = int(min_sup * m2)
        else:
            count1 = sup2
        sup3 = round(M[2, 3] * con_info[key1][3])
        if sup3 >= min_sup * m3:
            count2 = int(min_sup * m3)
        else:
            count2 = sup3
        con_info[key1] = [count, count1, count2, FI['4'][key1]]
    else:
        con_info[key1][3] = FI['4'][key1]
    # 打印候选项集
    # print(key1, ':', con_info[key1][0] + con_info[key1][1] + con_info[key1][2] + con_info[key1][3])
    if con_info[key1][0] + con_info[key1][1] + con_info[key1][2] + con_info[key1][3] >= min_sup * (n + n1):
        final_FI[key1] = con_info[key1][0] + con_info[key1][1] + con_info[key1][2] + con_info[key1][3]
# 原来频繁现不频繁
for key2 in all_FI.keys() - FI['4']:
    sup4 = 1/3 * (round(M[0, 3] * con_info[key2][0])+round(M[1, 3] * con_info[key2][1])+round(M[2, 3] * con_info[key2][2]))
    if sup4 >= min_sup * n1:
        count3 = int(min_sup * n1)
    else:
        count3 = sup4
    con_info[key2][3] = count3
    # 打印候选项集
    # print(key2, ':', con_info[key2][0] + con_info[key2][1] + con_info[key2][2])
    if con_info[key2][0] + con_info[key2][1] + con_info[key2][2] + con_info[key2][3] >= min_sup * (n + n1):
        final_FI[key2] = con_info[key2][0] + con_info[key2][1] + con_info[key2][2] + con_info[key2][3]
time_end2 = time.perf_counter()
print('数据库更新后的挖掘的个数为：', len(final_FI))
print('更新后为',final_FI)
print('新增数据库后挖掘时间为：', time_end2 - time_end1, 's')
print('总的挖掘时间为：',time_end2 - time_start, 's')
