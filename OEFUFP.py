# EFUFP 原始数据库的挖掘
import FPTree,FPNode
import time
## 动态构建BSW列表，BSW的个数是事先固定好的
# BSW = globals()
# for m in range(1, 4):
#     BSW[str(m)] = []
# num = 0
# with open(r'C:\Users\Administrator\Desktop\data\T10I4D100K.txt') as database:
#     for line in database:
#         num += 1
#         if num in range(1, 20001):
#             BSW[str(1)].append(line.split())
#         elif num in range(20001, 40001):
#             BSW[str(2)].append(line.split())
#         else:
#             BSW[str(3)].append(line.split())
  # n为滑动窗口的大小
def find_frequent_items(data_set,n,include_support=False):
    # n = 20000
    # 获取1项集及其支持度
    def get_item1(data_set):
        rect = {}
        for line in data_set:
            for item in line:
                rect[item] = rect.get(item, 0) + 1
        return rect
    # 项目降序排列
    def descending(rect):
        tp_list = []
        tp_list.extend(rect.keys())  # 列表的扩展，即将两个列表合并成一个
        tp_list.sort(key=lambda x: rect[x], reverse=True)
        tp_dict = {}
        i = 1
        for item in tp_list:
            tp_dict[item] = i
            i += 1
        return tp_dict
    # 事务排序后带有计数
    def count_order(rect, tp_dict):
        for elem in tp_dict:
            if elem in rect:
                tp_dict[elem] = rect[elem]
        return tp_dict
    # 2.获得1项集计数
    ys_item1 = get_item1(data_set)
    # 3.事务按从大到小排序
    tp_list = []
    tp_list.extend(ys_item1.keys())
    tp_list.sort(key=lambda x: ys_item1[x], reverse=True)
    tp_dict = {}
    i = 1
    for item in tp_list:
        tp_dict[item] = i
        i += 1
    ys_item1_order = count_order(rect=ys_item1, tp_dict=tp_dict)

    # 4.把项目分别加入大项目表和小项目表
    #####################
    min_sup = 0.01
    big_table = {}
    small_table = {}
    for item in tp_list:
        if ys_item1[item] >= min_sup * n:
            big_table[item] = ys_item1[item]
        else:
            small_table[item] = ys_item1[item]
    # 5.根据big_table建树
    tree = FPTree.FPTree()
    for line in data_set:
        line = list(filter(lambda v: v in big_table, line))
        line.sort(key=lambda x: big_table[x], reverse=True)
        tree.add(line)
    # =================================挖掘频繁项集==============================
    # print('开始挖掘:')
    def pf_item(paths, min_sup):
        rect = {}
        for path in paths:
            condition_node = path.pop(0)
            for item in path:
                rect[item] = rect.get(item, 0) + condition_node[1]
        rect1 = {}
        for item in rect:
            if rect[item] >= min_sup:
                rect1[item] = rect[item]
        rect_dict = descending(rect1)
        return rect1, rect_dict

    def tjms_tree(paths, rect1, rect_dict):
        # 建树
        treep = FPTree.FPTree()
        for path in paths:
            condition_node = path.pop(0)
            path = list(filter(lambda v: v in rect1, path))
            path.sort(key=lambda x: rect_dict[x])
            point = treep.root
            for item in path:
                next_point = point.search(item)
                if next_point:
                    next_point.count += condition_node[1]
                else:
                    next_point = FPNode.FPNode(treep, item, condition_node[1])
                    point.add(next_point)
                    treep._update_route(next_point)
                point = next_point

        return treep

        # 找到后缀

    def find_with_suffix(tree, suffix):
        for item, node in tree.items():
            support = sum(n.count for n in node)
            if support >= min_sup and item not in suffix:  # item不在fuffix中
                found_set = [item] + suffix  # 把item放入到suffix的最前
                yield (found_set, support) if include_support else found_set

                # 构建条件树并递归搜索频繁其中的项目集
                rect1, rect_dict = pf_item(tree.prefix_paths(item), min_sup * n)
                cond_tree = tjms_tree(tree.prefix_paths(item), rect1, rect_dict)
                for s in find_with_suffix(cond_tree, found_set):
                    yield s
    for itemset in find_with_suffix(tree, []):
        yield itemset
    # print('原始数据库挖掘的条数为：', len(final))
    # # print(final)
    # print('原始数据库的运行时间为：', time_end1-time_start, 's')
# if __name__ == '__main__':
#     FI = []
#     time_start = time.perf_counter()
#     # min_sup = 0.19
#     # 每个BSW分别调用FIU找到频繁项集
#     FI = globals()
#     for m in range(1, 4):
#         frequent_itemsets = find_frequent_items(BSW[str(m)], include_support=True)
#         FI[str(m)] = []
#         for itemset, support in frequent_itemsets:  # 将generator结果存入list
#             if len(itemset) != 1:
#                 FI[str(m)].append((itemset, support))
#         result = sorted(FI[str(m)], key=lambda support: support[1])  # 排序后输出
#         print('频繁项集的个数为：',len(result))
#         # if m == 1:
#         #     for itemset, support in FI[str(1)]:
#         #         if len(itemset) != 1:
#         #             print(str(itemset) + ': ' + str(support))
#     time_end = time.perf_counter()
#     print('运行时间为：', time_end - time_start)
