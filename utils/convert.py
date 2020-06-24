import math


def hex_to_timestamp(hex_field):
    """
    # 十六进制字段转化为时间戳
    :param hex_field: 十六进制字段
    :return: 十六进制字段对应的时间戳
    """
    seconds_part = int(hex_field[:8], 16)  # 十六进制秒转化为十进制秒，整数秒
    sub_seconds_part = int(hex_field[8:], 16)
    sub_seconds_part_dec = sub_seconds_part * 25 / 1e+6  # 十六进制亚秒转化为十进制秒，小数秒
    timestamp = seconds_part + sub_seconds_part_dec  # 整数秒加上小数秒得到时间戳
    return timestamp


def timestamp_to_hex(timestamp):
    """
    # 时间戳转化为十六进制
    :param timestamp: 时间戳
    :return: 时间戳对应的十六进制字段
    """
    if timestamp < 0:  # 如果输入的时间戳是负数，则首先转化为正数
        timestamp *= -1

    timestamp_list = math.modf(timestamp)  # 分割整数位和小数位
    four_byte_second = hex(int(timestamp_list[1]))  # 返回的是字符串
    two_byte_sub_second = hex(int(timestamp_list[0] * 1e+6 / 25))  # 小数位*1e+6转化为微秒，再除以25得到亚秒

    # 毫秒和微妙太小，导致亚秒对应的十六进制位不足2B，如'0xab'，考虑在前面补充'00'，填补成两个字节，成为'0x00ab'
    if len(two_byte_sub_second) <= 3:  # 如果毫秒和微秒设置太小，则补 '000'，变成 b'0007'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '000' + two_byte_sub_second[2:]
    elif len(two_byte_sub_second) == 4:  # 如果毫秒和微秒设置太小，则补 '00'，变成 b'007b'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '00' + two_byte_sub_second[2:]
    elif len(two_byte_sub_second) == 5:  # 如果微秒为0，则补一个字符 '0'，变成 b'07bd'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '0' + two_byte_sub_second[2:]
    else:  # 显示两个字节，则直接返回
        two_byte_sub_second = two_byte_sub_second

    # # 如果输入的时间戳是负数
    # if four_byte_second[:1] == '-':  # 出现'-0x76892342'，这是由于时间戳递减导致的
    #     four_byte_second = four_byte_second[1:]
    # if two_byte_sub_second[:1] == '-':
    #     two_byte_sub_second = two_byte_sub_second[1:]

    str_byte_second = four_byte_second[2:] + two_byte_sub_second[2:]  # 截取后面字符拼接为6B十六位字符
    return str_byte_second.encode('utf-8')  # 将str转化为hex，如'abcd'转化为 b'abcd'


if __name__ == "__main__":
    hex_field = b'5ef1beb79bff'
    print("hex field : %s " % hex_field)
    timestamp_from_hex = hex_to_timestamp(hex_field)
    print("timestamp from hex : %s " % timestamp_from_hex)
    hex_from_timestamp = timestamp_to_hex(timestamp_from_hex)
    print("timestamp to hex : %s " % hex_from_timestamp)

    timestamp_field = -1592901303.998375
    hex_from_timestamp = timestamp_to_hex(timestamp_field)
    print("hex from timestamp : %s " % hex_from_timestamp)
