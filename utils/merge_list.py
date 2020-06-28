

def merge(list1, list2):
    """
    合并两个有序的列表成为一个有序的列表。本方法采用从后往前合并
    :param list1: 有序列表1
    :param list2: 有序列表2
    :return: 合并后的有序列表
    """
    i = len(list1) - 1  # 用于记录第一个有序列表的最后一个待合并的元素索引
    j = len(list2) - 1  # 用于记录第二个有序列表的最后一个待合并的元素索引
    k = len(list1) + len(list2) - 1  # 用于记录合并后有序列表的最后一个元素的索引
    list3 = [0] * (len(list1) + len(list2))  # 用于存储最后合并后的有序列表

    while i >= 0 and j >= 0:  # 如果两个列表都没有合并完
        if list1[i] > list2[j]:  # 如果第一个有序列表当前最后一个元素大于第二个有序列表的
            list3[k] = list1[i]  # 把第一个有序列表的当前最后一个元素合并到列表3
            k -= 1  # 列表3往前移动一位
            i -= 1  # 列表1往前移动一位
        else:  # 如果第二个有序列表当前最后一个元素大于第一个有序列表的
            list3[k] = list2[j]  # 把第二个有序列表的当前最后一个元素合并到列表3
            k -= 1  # 列表3往前移动一位
            j -= 1  # 列表2往前移动一位

    while j >= 0:  # 如果列表2没有合并完，但是列表1合并完了
        list3[k] = list2[j]  # 将列表2的元素依次合并到列表3
        k -= 1
        j -= 1

    while i >= 0:  # 如果列表1没有合并完，但是列表2合并完了
        list3[k] = list1[i]  # 将列表1的元素依次合并到列表3
        k -= 1
        i -= 1

    # print(k,i,j)  # 此时k=-1, i=-1, j=-1

    return list3


if __name__ == "__main__":
    list2 = [2, 4, 7, 9, 12]
    list1 = [1, 3, 5, 6, 8, 10, 11]
    list3 = merge(list1=list1, list2=list2)
    print(list3)

    x = b'0001'
    y = b'000a'
    print(x[2:] < y[2:])
