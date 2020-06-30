import binascii
import mmap

from utils import new_hex, view_hex, repair_hex, statistics
import json


def converge(odd_file, even_file, intact_file, sync_header_odd, sync_footer_odd, sync_header_even, sync_footer_even):
    """
    合并两个十六进制文件成为一个十六进制文件，采用交替合并的方法
    :param odd_file: 第一个十六进制文件，默认头文件为合并后十六进制文件的头文件
    :param even_file: 第二个十六进制文件
    :param intact_file: 合并后的十六进制文件
    :param sync_header_odd: 第一个文件的搜索头
    :param sync_footer_odd: 第一个文件的搜索尾
    :param sync_header_even: 第二个文件的搜索头
    :param sync_footer_even: 第二个文件的搜索尾
    :return: 合并成功返回 True
    """
    header_odd = binascii.unhexlify(sync_header_odd)  # 将默认的十六进制字符串的标识符搜索头，先转化为二进制字符串形式
    footer_odd = binascii.unhexlify(sync_footer_odd)  # 将默认的十六进制字符串的标识符搜索尾，先转化为二进制字符串形式
    content_odd = []  # 存储分割后的二进制文件到列表中，依次存放
    with open(odd_file, 'rb') as of:  # 以只读模式打开
        mm_odd = mmap.mmap(of.fileno(), 0, access=mmap.ACCESS_READ)  # 将文件的内容赋值给mm_odd
        current_offset_odd = 0  # 当前指针指向文件开头
        header_index_odd = mm_odd.find(header_odd, current_offset_odd)  # 从开头寻找header_odd
        footer_index_odd = mm_odd.find(footer_odd, current_offset_odd + len(header_odd))  # 从header-odd后寻找footer_odd
        if 0 <= header_index_odd < footer_index_odd:  # 如果找到一对 <header_odd, footer_odd>
            mm_odd.seek(header_index_odd)  # 将指针指向 header_odd 的位置，即 header_odd 的起始头坐标
            # 将 header_odd 头开始到 footer_odd头结束的内容赋值给body_odd
            body_odd = mm_odd.read(footer_index_odd - mm_odd.tell())
            content_odd.append(body_odd)  # 将 body_odd 追加到列表 content_odd 的末尾
            while body_odd is not None:  # 如果找到了一对 <header_odd, footer_odd> ，则继续
                current_offset_odd = mm_odd.tell()  # 将指针指向新位置，即，上次读取body_odd的末尾，footer_odd 的位置
                header_index_odd = mm_odd.find(header_odd, current_offset_odd)  # 往下再次从 footer_odd 寻找 header_odd
                # 往下再次从 footer_odd + len(header_odd) 寻找 footer_odd
                footer_index_odd = mm_odd.find(footer_odd, current_offset_odd + len(header_odd))
                if 0 <= header_index_odd < footer_index_odd:  # 如果又找到了一对
                    mm_odd.seek(header_index_odd)  # 指针指向当前 header_odd 的头位置
                    # 读取 header_odd 头到 footer_odd 头之间的内容，赋值给body_odd
                    body_odd = mm_odd.read(footer_index_odd - mm_odd.tell())
                    content_odd.append(body_odd)  # 将 body_odd 追加到列表 content_odd 的末尾
                else:  # 如果没有找到则结束循环
                    body_odd = None

        mm_odd.close()  # 关闭内存映射

    header_even = binascii.unhexlify(sync_header_even)  # 将默认的十六进制字符串的标识符搜索头，先转化为二进制字符串形式
    footer_even = binascii.unhexlify(sync_footer_even)  # 将默认的十六进制字符串的标识符搜索尾，先转化为二进制字符串形式
    content_even = []
    with open(even_file, 'rb') as ef:
        mm_even = mmap.mmap(ef.fileno(), 0, access=mmap.ACCESS_READ)
        current_offset_even = 0
        header_index_even = mm_even.find(header_even, current_offset_even)
        footer_index_even = mm_even.find(footer_even, current_offset_even + len(header_even))
        if 0 <= header_index_even < footer_index_even:
            mm_even.seek(header_index_even)
            body_even = mm_even.read(footer_index_even - mm_even.tell())
            content_even.append(body_even)
            while body_even is not None:
                current_offset_even = mm_even.tell()
                header_index_even = mm_even.find(header_even, current_offset_even)
                footer_index_even = mm_even.find(footer_even, current_offset_even + len(header_even))
                if 0 <= header_index_even < footer_index_even:
                    mm_even.seek(header_index_even)
                    body_even = mm_even.read(footer_index_even - mm_even.tell())
                    content_even.append(body_even)
                else:
                    body_even = None

        mm_even.close()

    for odd, even in enumerate(content_even):
        content_odd.insert(2 * odd + 1, even)

    contents = b''.join(content_odd)
    contents = binascii.hexlify(contents)
    new_hex.create_new(file_name=intact_file, content=contents)

    return content_odd



if __name__ == "__main__":
    content_odd = b'eb90abcd1234eb9083293243acdfeb9098003235'
    content_even = b'ff77dcba4321ff7720280088ff772839001feeac'
    odd_file = "../data/odd.dat"
    even_file = "../data/even.dat"
    new_hex.create_new(file_name=odd_file, content=content_odd)
    new_hex.create_new(file_name=even_file, content=content_even)
    print("odd file: ")
    view_hex.look_over(file_name=odd_file)
    print("even file: ")
    view_hex.look_over(file_name=even_file)

    intact_file = "../data/intact.dat"
    header_odd = b'eb90'
    footer_odd = b'eb90'
    header_even = b'ff77'
    footer_even = b'ff77'

    repair_hex.add_footer(file_name=odd_file, sync_header=footer_odd)
    repair_hex.add_footer(file_name=even_file, sync_header=footer_even)

    content_list = converge(odd_file=odd_file, even_file=even_file, intact_file=intact_file,
                            sync_header_odd=header_odd, sync_footer_odd=footer_odd, sync_header_even=header_even,
                            sync_footer_even=footer_even)
    print("intact file: ")
    view_hex.look_over(file_name=intact_file)

    repair_hex.delete_footer(file_name=odd_file, sync_header=footer_odd)
    repair_hex.delete_footer(file_name=even_file, sync_header=footer_even)
    print("odd file: ")
    view_hex.look_over(file_name=odd_file)
    print("even file: ")
    view_hex.look_over(file_name=even_file)

    d = statistics.count(content_list=content_list, identifier_list=[b'0832', b'ab', b'dc'], sync_header=b'eb90')
    print(d)

    with open('../data/result.json', 'a+') as f:
        json.dump(str(d), fp=f)
