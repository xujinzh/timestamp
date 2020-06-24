import binascii


def look_over(file_name):
    """
    # 查看十六进制文件的内容
    :param file_name: 文件的目录
    :return: 文件的内容
    """
    with open(file_name, "rb") as f:
        print(binascii.hexlify(f.read()))


if __name__ == "__main__":
    wechat_graph = '../data/wechatgraph.dat'
    look_over(file_name=wechat_graph)
