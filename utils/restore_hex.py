import binascii
import mmap

from utils import sum_list


def put_back(parent_sequence, sub_sequence, target_list, length_list):
    """
    把一个十六进制文件按照记录的提取位置和提取字段的长度放回原来的十六进制文件
    :param parent_sequence: 母序列，格式为十六进制文件路径
    :param sub_sequence: 子序列，格式为十六进制文件路径
    :param target_list: 从母序列提取子序列的位置记录，称为标记列表，各元素取整数
    :param length_list: 从母序列提取子序列的长度记录，与targeting_list一一对应，称为长度列表，各元素取整数
    :return: 返回放回/替换子序列之后的母序列
    """
    cum_length_list = sum_list.cumulative_sum(length_list=length_list, first_zero=True)  # 计算长度列表的累积和列表，首位元素插入 0

    with open(parent_sequence, "r+b") as pf:  # 以可读可写模式打开
        print("Length of Parent Sequence: %s " % len(binascii.hexlify(pf.read())))  # 打印文件总长度，以十六进制长度表示
        mmp = mmap.mmap(pf.fileno(), 0)  # 映射文件的所有内容

        with open(sub_sequence, "rb") as sf:  # 以只读模式打开
            print("Length of Sub-Sequence: %s " % len(binascii.hexlify(sf.read())))  # 打印文件总长度，以十六进制长度表示
            mms = mmap.mmap(sf.fileno(), 0, prot=mmap.PROT_READ)  # 以只读模式映射到地址空间

            for i in range(len(target_list)):  # 把子序列的内容按照标记列表和长度列表放回母序列相应位置
                mmp[target_list[i]:(target_list[i] + length_list[i])] = mms[cum_length_list[i]:cum_length_list[i + 1]]

            mms.close()

        mmp.close()


# if __name__ == "__main__":
#     p_seq = "../data/wechatgraph.dat"
#     s_seq = "../data/new.dat"
#     target_length = ([1, 2], [2, 4])
#     put_back(parent_sequence=p_seq, sub_sequence=s_seq, target_list=target_length[0], length_list=target_length[1])
