from datetime import datetime, timedelta

from utils import new_hex, view_hex, packet_correction

# 写内容到文件中，模拟源文件
wechatgraph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
primary_file = "../data/wechatgraph.dat"
new_hex.create_new(file_name=primary_file, content=wechatgraph)

# 查看源文件是否正确写入
print("ugly duckling : %s " % view_hex.look_over(file_name=primary_file))

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
                      moment=time, delta=delta)

# 查看源文件是否正确更正时间戳
print("white swan : %s " % view_hex.look_over(file_name=primary_file))
