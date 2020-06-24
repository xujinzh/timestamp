import binascii
import os

from utils import view_hex, new_hex


def add_footer(file_name, sync_header):
    """
    添加header/footer到文件结尾，方便replace_hex/extract_hex查找特定字段
    :param file_name: 文件名地址，以十六进制表示，如 b'eb906767'
    :param sync_header: 标识符，以十六进制表示，如 b'6767'
    :return: 返回内容末尾添加标识符的文件
    """
    footer = binascii.unhexlify(sync_header)  # 将十六进制字符串转化为二进制字符串
    with open(file_name, "a+b") as f:  # 以追加方式写入文件中
        f.write(footer)


def delete_footer(file_name, sync_header):
    """
    删除最后添加的footer，恢复文件内容
    :param file_name: 文件名地址，以十六进制表示，如 b'eb906767'
    :param sync_header: 标识符，以十六进制表示，如 b'6767'
    :return: 返回删除掉标识符的文件
    """

    for i in range(len(binascii.unhexlify(sync_header))):  # 以二进制字符串的形式从后一个一个删除字符，直到删除末尾的footer
        with open(file_name, "r+b") as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()


if __name__ == "__main__":
    test = b'67671828abcdeffa'
    file_name = '../data/test.dat'
    new_hex.create_new(file_name=file_name, content=test)
    footer = b'6767'
    print("before add footer: ")
    view_hex.look_over(file_name=file_name)

    add_footer(file_name=file_name, sync_header=footer)
    print("after add footer: ")
    view_hex.look_over(file_name=file_name)
    
    delete_footer(file_name=file_name, sync_header=footer)
    print("after delete footer: ")
    view_hex.look_over(file_name=file_name)
