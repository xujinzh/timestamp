from datetime import datetime, timedelta

from utils import new_hex, view_hex, extract_hex, repair_hex, replace_hex, restore_hex, drift_hex


def act(ugly_duckling, white_swan, sync_header, sync_footer, second_sync_header, second_sync_footer,
        moment=datetime.now(), delta=timedelta(microseconds=0), drift=True):
    """
    执行时间戳修改
    :param drift: 使用时间平移
    :param delta: 累加时间差量，时间戳格式
    :param moment: 起点时间
    :param second_sync_footer: 二级标识符尾，十六进制形式
    :param second_sync_header: 二级标识符头，十六进制形式
    :param sync_footer: 标识符尾，十六进制形式
    :param ugly_duckling: 修改前十六进制文件
    :param white_swan: 修改后十六进制文件
    :param sync_header: 标识符头，十六进制形式
    :return: 修改后文件
    """

    target_length = extract_hex.find_extract(file_name=ugly_duckling, header=sync_header, footer=sync_footer,
                                             new_file=white_swan)
    repair_hex.add_footer(file_name=white_swan, sync_header=second_sync_footer)
    if drift:
        drift_hex.find_drift(file_name=white_swan, header=second_sync_header, footer=second_sync_footer, moment=moment)
    else:
        replace_hex.find_replace(file_name=white_swan, header=second_sync_header, footer=second_sync_footer,
                                 moment=moment, delta=delta)
    repair_hex.delete_footer(file_name=white_swan, sync_header=second_sync_footer)
    restore_hex.put_back(parent_sequence=ugly_duckling, sub_sequence=white_swan, targeting_list=target_length[0],
                         length_list=target_length[1])


if __name__ == "__main__":
    # 写内容到文件中，模拟源文件
    wechatgraph = b'eb906767abcd45341495eb90676789005641fdeceb906767741685239562eb906767324501200032eb906767787645650205eb90'
    wechat_file = "../data/wechatgraph.dat"
    new_hex.create_new(file_name=wechat_file, content=wechatgraph)

    # 查看源文件是否正确写入
    print("wechatgraph : %s " % view_hex.look_over(file_name=wechat_file))

    # 找到介于标识符header=b'eb90'和footer=b'eb90'中的C包，提取到新文件中
    new_file = "../data/new.dat"
    targeting_length = extract_hex.find_extract(file_name=wechat_file, header=b'eb90', footer=b'eb90',
                                                new_file=new_file)
    print("targeting position : %s " % targeting_length[0])
    print("length information : %s " % targeting_length[1])

    # 查看提取的新文件
    print("new file : %s " % view_hex.look_over(file_name=new_file))

    # 添加footer到文件new.dat结尾
    footer = b'6767'
    repair_hex.add_footer(file_name=new_file, sync_header=footer)

    # 查看添加了footer的新文件
    print("new file after add footer : %s " % view_hex.look_over(file_name=new_file))

    # 替换时间戳。把介于标识符头header=b'6767'和footer=b'6767'中的时间戳更正，初始时间设为当前时间，累加时间设为delta，依次累加
    replace_hex.find_replace(file_name=new_file, header=b'6767', footer=b'6767', moment=datetime.now(),
                             delta=timedelta(microseconds=888))

    # 查看更正时间戳后的新文件内容。
    print("new file after correct timestamp : %s " % view_hex.look_over(file_name=new_file))

    # 删除最后添加的footer，保持文件内容
    repair_hex.delete_footer(file_name=new_file, sync_header=footer)

    # 查看最终更正时间戳后的新文件内容
    print("final new file after correct timestamp : %s " % view_hex.look_over(file_name=new_file))

    # 放回修改过时间码的new.dat到wechatgraph.dat相应位置
    restore_hex.put_back(parent_sequence=wechat_file, sub_sequence=new_file, targeting_list=targeting_length[0],
                         length_list=targeting_length[1])

    # 查看放回后的内容，以十六进制显示
    print("wechatgraph after correct timestamp : %s " % view_hex.look_over(file_name=wechat_file))
