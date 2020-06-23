import binascii
import mmap


def find_extract(file_name, header, footer, new_file):
    """
    从十六进制文件中查找特定的由多字节组成的字段，并提取到新文件，可能需要记录提取的位置
    :param file_name: 十六进制源文件
    :param header: 待查找的多字节字段头
    :param footer: 待查找的多字节字段尾
    :param new_file: 十六进制提取的文件
    :return: 返回提取的新文件，已经提取字段的标记位置列表和长度列表
    """
    header = binascii.unhexlify(header)  # 将默认的十六进制搜索头，先转化为文件处理形式
    footer = binascii.unhexlify(footer)  # 将默认的十六进制搜索尾，先转化为文件处理形式

    targeting = []  # 记录取数据的位置
    length = []  # 记录取数据的长度

    with open(file_name, "rb") as f:  # 以读方式打开文件
        #     print("Data: %s" % binascii.hexlify(f.read()))
        print("Length of Data by Hex Format: %s " % len(binascii.hexlify(f.read())))  # 打印文件总长度，以十六进制长度表示
        #     mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)  # 映射文件的所有内容
        current_offset = 0  # 开始指针位置为0
        header_index = mm.find(header, current_offset)  # 从current_offset开始向后去找header
        footer_index = mm.find(footer, current_offset + len(header))  # 从current_offset+len(header)开始向后找footer

        if 0 <= header_index < footer_index:  # 如果找到的header索引大于0，且footer出现在header后，即找到了匹配项
            # print("Found header at %s and footer at %s " % (header_index, footer_index))
            mm.seek(header_index + len(header))  # 将指针指向header后，如header_index=0, len(header)=2，则指向2

            # 考虑mm作为指针，当找到header时，指向header结尾，当read body后，指向body结尾位置。
            # 注意指针位置以un-hexlify(b'^\xe7\x04'、3位）来计算，而不是以hexlify(b'56ba'，4位)来计算

            targeting.append(mm.tell())

            body = mm.read(footer_index - mm.tell())  # 读从mm.tell()[即，header后]到footer之间的数据，赋值给body

            # 先清空待写入文件里的内容
            with open(new_file, "w+b") as nf:
                nf.truncate()

            # 将找到的内容追加写到文件中
            with open(new_file, "a+b") as nf:
                nf.write(body)

            length.append(len(body))

            while body is not None:
                # print("hexlify body: %s" % binascii.hexlify(body))
                current_offset = mm.tell()  # 将当前指针指向赋值给current_offset，其实就是上一个footer的位置
                header_index = mm.find(header, current_offset)  # 从footer字段后寻找header
                # print("current_offset + len(footer) : %s " % (current_offset + len(footer))) # 6
                footer_index = mm.find(footer, current_offset + len(header))  # 从比footer多header字节后寻找footer

                if 0 <= header_index < footer_index:  # 如果又找到了一对<header, footer>
                    # print("Found header at %s and footer at %s" % (header_index, footer_index))  # 打印header\footer位置
                    mm.seek(header_index + len(header))  # 将指针指向找到的header后位置，此时，mm.tell()指向找到的header后
                    targeting.append(mm.tell())

                    body = mm.read(footer_index - mm.tell())  # 将header和footer之间的内容赋值给body
                    # print(binascii.hexlify(body))
                    # 将找到的内容追加写到文件中
                    with open(new_file, "a+b") as nf:
                        nf.write(body)

                    length.append(len(body))

                else:  # 如果没有找到，结束循环
                    body = None  # 把 None 赋值给body
        mm.close()  # 关闭内存映射

    return targeting, length

# if __name__ == '__main__':
#     target_length = find_extract(file_name="./wechatgraph.dat", header="eb90", footer="eb90", new_file="./new.dat")
#     print("target list : %s " % target_length[0])
#     print("length list : %s " % target_length[1])
