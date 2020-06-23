import binascii
import mmap
from datetime import datetime, timedelta

from utils import correct_timestamp


def find_replace(file_name, header, footer, moment=datetime.now(),
                 delta=timedelta(seconds=0, milliseconds=0, microseconds=0)):
    """
    从十六进制文件中查找特定的由多字节组成的字段，并用设定的时间码替换某些特定的字段
    :param file_name: 十六进制源文件
    :param header: 待查找的多字节字段头
    :param footer: 待查找的多字节字段尾
    :param moment: 需要替换的时间码，以CST标准时间作为输入，通过调用utils.convert_time.time_hex_sec_subs转化为时间码，
                   并以十六进制表示，默认为代码编写时间
    :param delta: 每次累加的时间，以毫米累加，默认不累加
    :return: 返回替换后的文件
    """
    header = binascii.unhexlify(header)  # 将默认的十六进制搜索头，先转化为文件处理形式
    footer = binascii.unhexlify(footer)  # 将默认的十六进制搜索尾，先转化为文件处理形式

    with open(file_name, "r+b") as f:  # 以读写方式打开文件
        #     print("Data: %s" % binascii.hexlify(f.read()))
        # print("Length of Data: %s " % len(binascii.hexlify(f.read())))  # 打印文件总长度，以十六进制长度表示
        #     mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        mm = mmap.mmap(f.fileno(), 0)  # 映射文件的所有内容
        current_offset = 0  # 开始指针位置为0
        header_index = mm.find(header, current_offset)  # 从current_offset开始向后去找header
        footer_index = mm.find(footer, current_offset + len(header))  # 从current_offset+len(header)开始向后找footer

        if 0 <= header_index < footer_index:  # 如果找到的header索引大于0，且footer出现在header后，即找到了匹配项
            # print("Found header at %s and footer at %s" % (header_index, footer_index))
            mm.seek(header_index + len(header))  # 将指针指向header后，如header_index=0, len(header)=2，则指向2

            # 考虑mm作为指针，当找到header时，指向header结尾，当read body后，指向body结尾位置。
            # 注意指针位置以un-hexlify(b'^\xe7\x04'、3位）来计算，而不是以hexlify(b'56ba'，4位)来计算

            body = mm.read(footer_index - mm.tell())  # 读从mm.tell()[即，header后]到footer之间的数据，赋值给body
            second = correct_timestamp.time_hex_sec_subs(moment=moment)  # 计算时间的秒值

            #             mm[(mm.tell() - 6): (mm.tell() - 2)] = second[0]  # 替换 时间秒
            #             mm[(mm.tell() - 2):mm.tell()] = second[1]  # 替换 时间亚秒
            mm[header_index + len(header):header_index + len(header) + 4] = second[0]
            mm[header_index + len(header) + 4:header_index + len(header) + 6] = second[1]

            # while body is not None:
            while len(binascii.hexlify(body)) > 6:  # 因为要修改时间戳(4B+2B=6B），所以最少要6位
                # print("hexlify body: %s" % binascii.hexlify(body))
                current_offset = mm.tell()  # 将当前指针指向赋值给current_offset，其实就是上一个footer的位置
                header_index = mm.find(header, current_offset)  # 从footer字段后寻找header
                footer_index = mm.find(footer, current_offset + len(header))  # 从比footer多header字节后寻找footer
                if 0 <= header_index < footer_index:  # 如果又找到了一对<header, footer>
                    # print("Found header at %s and footer at %s" % (header_index, footer_index))  # 打印header\footer位置
                    mm.seek(header_index + len(header))  # 将指针指向找到的header后位置，此时，mm.tell()指向找到的header后
                    body = mm.read(footer_index - mm.tell())  # 将header和footer之间的内容赋值给body
                    delta = delta + delta
                    second = correct_timestamp.time_hex_sec_subs(moment=moment, delta=delta)  # 计算累加后时间的秒值
                    #                     mm[(mm.tell() - 6): mm.tell() - 2] = second[0]  # 替换 时间秒
                    #                     mm[mm.tell() - 2:mm.tell()] = second[1]  # 替换 时间亚秒
                    mm[header_index + len(header):header_index + len(header) + 4] = second[0]
                    mm[header_index + len(header) + 4:header_index + len(header) + 6] = second[1]
                else:  # 如果没有找到，则赋值给body为"00"，即，结束循环
                    body = binascii.unhexlify("00")  # 把"00"按照非十六进制的形式赋值给body
        mm.close()  # 关闭内存映射

# if __name__ == '__main__':
#     time = datetime(2020, 6, 17, 12, 48, 55, 100388)
#     delta = timedelta(seconds=0, milliseconds=0, microseconds=300)
#     find_replace(file_name="./wechatimage.dat", header="5653", footer="8383", moment=time, delta=delta)
#     time_hex = time_hex_sec_subs(moment=time, delta=delta)
#     print(binascii.hexlify(time_hex[0]))
#     print(binascii.hexlify(time_hex[1]))
