import binascii

from utils import view_hex


def create_new(file_name, content):
    """
    写内容到文件中，模拟源文件，以十六进制保存
    :param file_name: 保存文件的目录
    :param content: 写入的十六进制内容，如 b'6767'
    :return: 写入成功返回True
    """

    with open(file_name, 'w+b') as f:
        f.write(binascii.unhexlify(content))

    return True


if __name__ == "__main__":
    wechat_graph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
    file_name = '../data/wechatgraph.dat'
    create_new(file_name=file_name, content=wechat_graph)
    view_hex.look_over(file_name)

