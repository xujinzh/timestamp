import binascii
import mmap

from utils import new_hex, view_hex


def find_extract(file_name, header, footer, new_file):
    """
    从十六进制文件中查找特定的由多字节组成的字段，并提取到新文件，同时记录提取的位置和提取的二进制字符串长度
    :param file_name: 十六进制源文件
    :param header: 待查找的标识符搜索头
    :param footer: 待查找的标识符搜索尾
    :param new_file: 提取的十六进制文件
    :return: new_file 返回提取的新文件，以及提取的字段的标记位置列表和长度列表
    """
    header = binascii.unhexlify(header)  # 将默认的十六进制字符串的标识符搜索头，先转化为二进制字符串形式
    footer = binascii.unhexlify(footer)  # 将默认的十六进制字符串的标识符搜索尾，先转化为二进制字符串形式

    targeting = []  # 记录提取的二进制字符串的位置，以二进制字符串头为准
    length = []  # 记录提取的二进制字符串的长度，与targeting一一对应，即 len(targeting) == len(length)
    content_list = []  # 以列表的形式记录提取的内容，二进制字符串格式

    with open(file_name, "rb") as f:  # 以只读方式打开二进制文件
        #     print("Data: %s" % binascii.hexlify(f.read()))
        print("文件总长度(以十六进制字符串长度显示）: %s " % len(binascii.hexlify(f.read())))  # 打印文件总长度，以十六进制长度表示
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)  # 映射文件的所有内容
        current_offset = 0  # 开始指针位置为0
        header_index = mm.find(header, current_offset)  # 从current_offset开始向后寻找header
        footer_index = mm.find(footer, current_offset + len(header))  # 从current_offset+len(header)开始向后寻找footer

        if 0 <= header_index < footer_index:  # 如果找到的header索引大于0，且footer出现在header后，即找到了匹配项
            # print("Found header at %s and footer at %s " % (header_index, footer_index))
            mm.seek(header_index + len(header))  # 将指针指向header后，如header_index=0, len(header)=2，则指向2

            # 考虑mm作为指针，当找到header时，指向header结尾，当read body后，指向body结尾位置。
            # 注意指针位置以un-hexlify(b'^\xe7\x04'、3位）来计算，而不是以hexlify(b'56ba'，4位)来计算

            targeting.append(mm.tell())  # targeting 中记录的是截取二进制字符串的开始位置
            # 从mm.tell()开始读footer_index-mm.tell()个二进制字符串。
            body = mm.read(footer_index - mm.tell())  # 读从mm.tell()[即，header后]到footer之间的数据，赋值给body
            content_list.append(body)
            # 先清空待写入文件里的内容
            with open(new_file, "w+b") as nf:
                nf.truncate()

            # 将找到的内容追加写到文件中
            with open(new_file, "a+b") as nf:
                nf.write(body)

            length.append(len(body))  # length 中记录的是截取的二进制字符串的长度

            while body is not None:
                current_offset = mm.tell()  # 将当前指针指向赋值给current_offset，其实就是上一个footer的位置
                header_index = mm.find(header, current_offset)  # 从footer字段后寻找header
                footer_index = mm.find(footer, current_offset + len(header))  # 从比footer多一个header长度后寻找footer

                if 0 <= header_index < footer_index:  # 如果又找到了一对<header, footer>
                    # print("Found header at %s and footer at %s" % (header_index, footer_index))  # 打印header\footer位置
                    mm.seek(header_index + len(header))  # 将指针指向找到的header后位置，此时，mm.tell()指向找到的header后
                    targeting.append(mm.tell())  # 记录找到的二进制字符串的位置

                    body = mm.read(footer_index - mm.tell())  # 将header和footer之间的内容赋值给body
                    content_list.append(body)
                    # 将找到的内容追加写到文件中
                    with open(new_file, "a+b") as nf:
                        nf.write(body)

                    length.append(len(body))  # 记录找到的二进制字符串的长度

                else:  # 如果没有找到，结束循环
                    body = None  # 把 None 赋值给body
        mm.close()  # 关闭内存映射

    return targeting, length, content_list


if __name__ == '__main__':
    # 写内容到文件中，模拟源文件
    wechatgraph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
    wechat_file = "../data/wechatgraph.dat"
    new_hex.create_new(file_name=wechat_file, content=wechatgraph)

    new_file = "../data/new.dat"
    target_length = find_extract(file_name=wechat_file, header="eb90", footer="eb90", new_file=new_file)
    print("target list : %s " % target_length[0])
    print("length list : %s " % target_length[1])

    view_hex.look_over(wechat_file)
    view_hex.look_over(new_file)
    print("content: %s" % target_length[2])
    for content in target_length[2]:
        print(binascii.hexlify(content))
