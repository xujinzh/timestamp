import binascii
import math
from datetime import datetime, timedelta

from utils import feature_match


def time_hex_sec_subs(moment=None,
                      delta=timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0),
                      show_timestamp=False):
    """
    输入一个时间，datetime类型，输出其对应的十六进制字符串，4B表示秒，2B表示亚秒（不足2B部分前面填充0）
    :param moment: datetime 类型，默认为None，当前时间，格式为 年(years)，月(months)，日(days)，时(hours)，分(minutes)，秒(seconds)，
                   微秒(microseconds)，共7个参数
    :param delta: timedelta 类型，默认为0微秒，格式为 天（days），秒（seconds），微秒（microseconds），毫秒（milliseconds），分（minutes），
                   时（hours），星期（weeks）
    :param show_timestamp: boolean 类型，默认为 False，表示是否打印时间戳
    :return: 十六进制字符串，4B 表示秒 seconds，2B 表示亚秒 sub-seconds
    """
    if moment is None:  # 如果缺失时间，则默认是当前时间，精确到微秒
        cst_time = datetime.now() + delta
        cst_timestamp = cst_time.timestamp()
        if show_timestamp:
            print("timestamp of now : %s " % cst_timestamp)
    else:  # 如果输入自定义时间，则使用自定义时间
        moment += delta
        cst_timestamp = moment.timestamp()  # convert CST time to timestamp
        if show_timestamp:
            print("timestamp of input moment : %s " % cst_timestamp)

    timestamp_list = math.modf(cst_timestamp)  # 分割时间戳的整数位和小数位，以元组表示，分别是(小数位，整数位）
    four_byte_second = hex(int(timestamp_list[1]))  # 将整数位转化为字符串型十六进制数
    sub_second = timestamp_list[0] * 1e+6 / 25  # 小数位 *1e+6 转化为微秒，再除以25得到亚秒
    two_byte_sub_second = hex(int(sub_second))  # 将小数位转化为字符串型十六进制数

    if four_byte_second[:1] == '-':  # 出现'-0x76892342'，这可能是由于时间戳递减导致的
        four_byte_second = four_byte_second[1:]  # 那么只取符号后的字符串型十六进制数
    if two_byte_sub_second[:1] == '-':
        two_byte_sub_second = two_byte_sub_second[1:]

    # 将亚秒部分不足两个字节的字符串型十六进制数转化为统一的2B字符串型十六进制数
    two_byte_sub_second = feature_match.convert_to_double_byte(two_byte_sub_second)

    # 分别返回整数秒部分和小数亚秒部分的二进制字符串
    return binascii.unhexlify(four_byte_second[2:]), binascii.unhexlify(two_byte_sub_second[2:])


if __name__ == '__main__':
    moment = datetime(2020, 6, 17, 10, 33, 56, 0)
    delta = timedelta(seconds=3, milliseconds=902, microseconds=200)
    result = time_hex_sec_subs(moment=moment, delta=delta)
    print("integer part of unhex at moment + delta : %s " % result[0])
    print("integer part of hexlify at moment + delta : %s " % binascii.hexlify(result[0]))
    print("decimal part of unhex at moment + delta : %s " % result[1])
    print("decimal part of hexlify at moment + delta : %s " % binascii.hexlify(result[1]))

    now_result = time_hex_sec_subs(show_timestamp=True)  # 当前时间
    first = now_result[0]
    second = now_result[1]
    print("binascii.hexlify(integer part) at now : %s " % binascii.hexlify(first))
    print("binascii.hexlify(decimal part ) at now : %s " % binascii.hexlify(second))
