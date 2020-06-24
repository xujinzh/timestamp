import math
from utils import feature_match


def hex_to_timestamp(hex_field):
    """
    # 十六进制字符串转化为时间戳
    :param hex_field: 十六进制字符串
    :return: 十六进制字符串对应的时间戳
    """
    seconds_part = int(hex_field[:8], 16)  # 十六进制字符串秒转化为十进制字符串秒，该字符串表示整数秒
    sub_seconds_part = int(hex_field[8:], 16)  # 十六进制字符串秒转化为十进制字符串秒，该字符串表示亚秒
    sub_seconds_part_dec = sub_seconds_part * 25 / 1e+6  # 亚秒转化为小数秒
    timestamp = seconds_part + sub_seconds_part_dec  # 整数秒加上小数秒得到时间戳数
    return timestamp


def timestamp_to_hex(timestamp):
    """
    # 时间戳数转化为十六进制字符串
    :param timestamp: 时间戳数
    :return: 时间戳对应的十六进制字符串
    """
    if timestamp < 0:  # 如果输入的时间戳数是负值
        timestamp *= -1  # 则转化为正数

    timestamp_list = math.modf(timestamp)  # 分割整数位和小数位成为元组，第一个位置是小数位，第二个位置是整数位
    four_byte_second = hex(int(timestamp_list[1]))  # 计算整数位的字符串型十六进制数
    sub_second = int(timestamp_list[0] * 1e+6 / 25)  # 小数位乘以1000000转化为微秒，再除以25得到亚秒
    two_byte_sub_second = hex(sub_second)  # 计算小数位的字符串型十六进制数
    two_byte_sub_second = feature_match.convert_to_double_byte(two_byte_sub_second)

    # # 如果输入的时间戳是负数
    # if four_byte_second[:1] == '-':  # 出现'-0x76892342'，这是由于时间戳递减导致的
    #     four_byte_second = four_byte_second[1:]
    # if two_byte_sub_second[:1] == '-':
    #     two_byte_sub_second = two_byte_sub_second[1:]

    str_byte_second = four_byte_second[2:] + two_byte_sub_second[2:]  # 截取后面字符拼接为6B十六位字符
    return str_byte_second.encode('utf-8')  # 将str转化为十六进制字符串，如'abcd'转化为 b'abcd'


if __name__ == "__main__":
    hex_field = b'5ef1beb700ff'
    print("hex field : %s " % hex_field)
    timestamp_from_hex = hex_to_timestamp(hex_field)
    print("timestamp from hex : %s " % timestamp_from_hex)
    hex_from_timestamp = timestamp_to_hex(timestamp_from_hex)
    print("timestamp to hex : %s " % hex_from_timestamp)

    timestamp_field = -1592901303.006375
    hex_from_timestamp = timestamp_to_hex(timestamp_field)
    print("hex from timestamp : %s " % hex_from_timestamp)
