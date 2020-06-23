def cumulative_sum(length_list, first_zero=False):
    """
    计算一个列表的累加序列，如输入是 [1, 2, 3]，输出是[1, 3, 6] 或 [0, 1, 3, 6]
    :param length_list: 待累加列表
    :param first_zero: boolean，标记是否在累加列表前增加 0，True 则增加，False 则不增加
    :return: 返回累加列表
    """
    cum_sum = 0  # 累加值
    if first_zero:  # 在累加列表前增加 0
        cum_length_list = [0]
    else:  # 在累加列表前不增加 0
        cum_length_list = []
    for i in length_list:
        cum_sum += i
        cum_length_list.append(cum_sum)
    return cum_length_list


# if __name__ == "__main__":
#     length_list = [1, 2, 3]
#     print("不增加 0 : %s " % cumulative_sum(length_list=length_list))
#     print("增加 0 : %s " % cumulative_sum(length_list=length_list, first_zero=True))
