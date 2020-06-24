import binascii
import mmap
from datetime import datetime

from utils import convert, new_hex, view_hex, extract_hex, repair_hex


def find_drift(file_name, header, footer, moment=datetime.now()):
    """
    从十六进制文件中查找特定标识符后由6B组成的时间码字段，并用设定的时间码作为开始时间码，依次平移/漂移以后的所有时间码
    :param file_name: 十六进制源文件
    :param header: 待查找的标识符搜索头，格式为十六进制字符串，如 b'1b82'
    :param footer: 待查找的标识符搜索尾，格式位十六进制字符串，如 b'2b83'
    :param moment: 需要替换的时间码，以CST标准时间作为输入，首先转化为十六进制字符串，默认当前时间
    :return: 返回替换后的十六进制文件
    """
    header = binascii.unhexlify(header)  # 将默认的十六进制字符串型标识符搜索头，先转化为二进制字符串
    footer = binascii.unhexlify(footer)  # 将默认的十六进制字符串型标识符搜索尾，先转化为二进制字符串

    with open(file_name, "r+b") as f:  # 以读写方式打开文件
        #     print("Data: %s" % binascii.hexlify(f.read()))
        #     mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        mm = mmap.mmap(f.fileno(), 0)  # 映射文件的所有内容到地址空间
        current_offset = 0  # 开始指针位置为0，指向文件开始
        header_index = mm.find(header, current_offset)  # 从current_offset开始向后寻找header
        footer_index = mm.find(footer, current_offset + len(header))  # 从current_offset+len(header)开始向后寻找footer

        if 0 <= header_index < footer_index:  # 如果找到的header索引大于0，且footer出现在header后，即找到了匹配项
            # print("Found header at %s and footer at %s" % (header_index, footer_index))
            mm.seek(header_index + len(header))  # 将指针指向header后，如header_index=0, len(header)=2，则指向2，记住是二进制形式查找

            # 考虑mm作为指针，当找到header时，指向header结尾，当read body后，指向body结尾位置。
            # 注意指针位置以二进制字符串un-hexlify(b'^\xe7\x04'、3位）来计算，而不是以十六进制字符串hexlify(b'56ba'、4位)来计算

            body = mm.read(footer_index - mm.tell())  # 读从mm.tell()[即，header后]到footer之间的数据，赋值给body
            body_timestamp = convert.hex_to_timestamp(binascii.hexlify(body))  # 将二进制字符串时间戳字段body转化为时间戳数
            moment_timestamp = moment.timestamp()  # 获取开始时间(设定的时间）的时间戳
            delta_drift = moment_timestamp - body_timestamp  # 计算第一帧时间戳与设定的时间的时间戳的差值

            # second = correct_timestamp.time_hex_sec_subs(moment=moment)  # 计算时间的秒值
            # mm[header_index + len(header):header_index + len(header) + 4] = second[0]
            # mm[header_index + len(header) + 4:header_index + len(header) + 6] = second[1]

            moment_hex = binascii.unhexlify(convert.timestamp_to_hex(moment_timestamp))  # 将设定时间的时间戳转化为二进制字符串
            # 二进制字符串的长度的等于 6，时间码是6B = 4B + 2B，必须保证 len(body) == len(moment_hex)；把新时间戳赋值给第一帧时间戳所在的位置
            mm[header_index + len(header):header_index + len(header) + len(body)] = moment_hex

            # while body is not None:
            while len(binascii.hexlify(body)) > 6:  # 因为要修改时间戳(4B + 2B = 6B），所以最少要6位
                current_offset = mm.tell()  # 将当前指针指向赋值给current_offset，其实就是上一个footer的位置
                header_index = mm.find(header, current_offset)  # 从footer字段后寻找header
                footer_index = mm.find(footer, current_offset + len(header))  # 从比footer多header字节后寻找footer
                if 0 <= header_index < footer_index:  # 如果又找到了一对<header, footer>
                    mm.seek(header_index + len(header))  # 将指针指向找到的header后的位置，此时，mm.tell()指向找到的header后
                    body = mm.read(footer_index - mm.tell())  # 将header和footer之间的二进制字符串赋值给body
                    body_timestamp = convert.hex_to_timestamp(binascii.hexlify(body))  # 将二进制字符串转化为时间戳
                    moment_timestamp = body_timestamp + delta_drift  # 计算时间飘移后的时间戳

                    # moment = datetime.fromtimestamp(moment_timestamp)
                    # second = correct_timestamp.time_hex_sec_subs(moment=moment)  # 计算累加后时间的秒值
                    # mm[header_index + len(header):header_index + len(header) + 4] = second[0]
                    # mm[header_index + len(header) + 4:header_index + len(header) + 6] = second[1]

                    moment_hex = binascii.unhexlify(convert.timestamp_to_hex(moment_timestamp))  # 时间戳转化为二进制字符串
                    mm[header_index + len(header):header_index + len(header) + len(body)] = moment_hex  # 二进制字符串赋值给时间戳位置
                else:  # 如果没有找到，则赋值b"00"给body，即，结束循环
                    body = binascii.unhexlify(b"00")  # 把"00"按照非十六进制的形式赋值给body
        mm.close()  # 关闭内存映射


if __name__ == '__main__':
    # 写内容到文件中，模拟源文件
    wechatgraph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
    wechat_file = "../data/wechatgraph.dat"
    new_hex.create_new(file_name=wechat_file, content=wechatgraph)

    new_file = "../data/test.dat"
    extract_hex.find_extract(file_name=wechat_file, header=b'eb90', footer=b'eb90', new_file=new_file)

    view_hex.look_over(new_file)
    repair_hex.add_footer(file_name=new_file, sync_header=b'6767')
    find_drift(new_file, b'6767', b'6767', moment=datetime.now())
    repair_hex.delete_footer(file_name=new_file, sync_header=b'6767')
    view_hex.look_over(new_file)
