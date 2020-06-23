import binascii
import os

from utils import view_hex, new_hex


def add_footer(file_name, sync_header):
    """
    添加header/footer到文件结尾，方便replace_hex/extract_hex查找特定字段
    :param file_name: 文件名地址，以十六进制表示，如 b'6767'
    :param sync_header: 标识符
    :return: 返回内容末尾添加标识符的文件
    """
    footer = binascii.unhexlify(sync_header)
    with open(file_name, "a+b") as f:
        f.write(footer)


def delete_footer(file_name, sync_header):
    """
    删除最后添加的footer，恢复文件内容
    :param file_name: 文件名地址，以十六进制表示，如 b'6767'
    :param sync_header: 标识符
    :return: 返回删除掉标识符的文件
    """

    for i in range(len(binascii.unhexlify(sync_header))):
        with open(file_name, "r+b") as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()


# if __name__ == "__main__":
#     test = b'67671828abcdeffa'
#     file_name = '../data/test.dat'
#     new_hex.create_new(file_name=file_name, content=test)
#     footer = b'6767'
#     content_before = view_hex.look_over(file_name=file_name)
#     print("before add footer : %s" % content_before)
#
#     add_footer(file_name=file_name, sync_header=footer)
#     content_after = view_hex.look_over(file_name=file_name)
#     print("after add footer : %s " % content_after)
#
#     delete_footer(file_name=file_name, sync_header=footer)
#     content_delete_footer = view_hex.look_over(file_name=file_name)
#     print("after delete footer : %s " % content_delete_footer)
