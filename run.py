from datetime import datetime, timedelta

from utils import new_hex, view_hex, packet_correction

"""
本代码术语约定:

b'abcd0023': 此类型数据称为十六进制字符串，可以通过 binascii.hexlify(b'\xab\xcd\x004') 将二进制字符串转化为十六进制字符串
b'\xab\xcd\x004' : 此类型数据称为二进制字符串，可以通过 binascii.unhexlify(b'abcd0034') 将十六进制字符串转化为二进制字符串
2020-06-24 14:27:03.118613 : 此数据类型称为 datetime数，由 datetime() 函数生成
1592980107.131059 : 此数据类型称为时间戳数，由 datetime().timestamp() 函数生成
0x5ef1beb7 : 此数据称为字符串型十六进制数，有python内建函数hex()生成，将十进制整数(int)转化为带有'0x'标识的十六进制数，类型是str
"""

# 写内容到文件中，模拟源文件
wechatgraph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
primary_file = "../data/wechatgraph.dat"
new_hex.create_new(file_name=primary_file, content=wechatgraph)

# 查看源文件是否正确写入
print("更正时间戳前的文件: ")
view_hex.look_over(file_name=primary_file)

# 找到介于标识符header=b'eb90'和footer=b'eb90'中的C包，提取到新文件中
secondary_file = "../data/new.dat"

first_header = b'eb90'
first_footer = b'eb90'
second_header = b'6767'
second_footer = b'6767'
time = datetime.now()
delta = timedelta(microseconds=888)

packet_correction.act(ugly_duckling=primary_file, white_swan=secondary_file, sync_header=first_header,
                      sync_footer=first_footer, second_sync_header=second_header, second_sync_footer=second_footer,
                      moment=time, delta=delta, drift=True)

# 查看源文件是否正确更正时间戳
print("更正时间戳后的文件: ")
view_hex.look_over(file_name=primary_file)
