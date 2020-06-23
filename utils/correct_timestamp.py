import binascii
import math
from datetime import datetime, timedelta


def time_hex_sec_subs(moment=None,
                      delta=timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0),
                      show_timestamp=False):
    """
    输入一个时间，输出其十六进制形式，4B表示秒，2B表示亚秒（不足2B部分前面填充0）
    :param moment: datetime 类型，默认为None，当前时间，格式为 年(year)，月(month)，日(day)，时(hour)，分(minute)，秒(second)，
                   微秒(microsecond)，共7个参数
    :param delta: timedelta 类型，默认为0微秒，格式为 天（days），秒（seconds），微秒（microseconds），毫秒（milliseconds），分（minutes），
                   时（hours），星期（weeks）
    :param show_timestamp: boolean 类型，默认为False，表示是否打印时间戳
    :return: hex timestamp with 4B seconds and 2B sub-seconds
    """
    if moment is None:  # 如果缺失时间，则默认是当前时间，精确到微秒
        cst_time = datetime.now() + delta
        cst_timestamp = cst_time.timestamp()
        if show_timestamp:
            print("timestamp of now : %s " % cst_timestamp)
    else:  # 如果输入自定义时间、时间戳，则使用自定义时间
        moment = moment + delta
        cst_timestamp = moment.timestamp()  # convert CST time to timestamp
        if show_timestamp:
            print("timestamp of input moment : %s " % cst_timestamp)

    timestamp_list = math.modf(cst_timestamp)  # 分割整数位和小数位
    four_byte_second = hex(int(timestamp_list[1]))  # 返回的是字符串
    two_byte_sub_second = hex(int(timestamp_list[0] * 1e+6 / 25))  # 小数位*1e+6转化为微秒，再除以25得到亚秒

    if len(two_byte_sub_second) <= 3:  # 如果毫秒和微秒设置太小，则补 '000'，变成 b'0007'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '000' + two_byte_sub_second[2:]
    elif len(two_byte_sub_second) == 4:  # 如果毫秒和微秒设置太小，则补 '00'，变成 b'007b'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '00' + two_byte_sub_second[2:]
    elif len(two_byte_sub_second) == 5:  # 如果微秒为0，则补一个字符 '0'，变成 b'07bd'的形式
        two_byte_sub_second = two_byte_sub_second[:2] + '0' + two_byte_sub_second[2:]
    else:  # 显示两个字节，则直接返回
        two_byte_sub_second = two_byte_sub_second
    if four_byte_second[:1] == '-':  # 出现'-0x76892342'，这是由于时间戳递减导致的
        four_byte_second = four_byte_second[1:]
    if two_byte_sub_second[:1] == '-':
        two_byte_sub_second = two_byte_sub_second[1:]
    return binascii.unhexlify(four_byte_second[2:]), binascii.unhexlify(two_byte_sub_second[2:])

# if __name__ == '__main__':
#     moment = datetime(2020, 6, 17, 10, 33, 56, 0)
#     delta = timedelta(seconds=3, milliseconds=902, microseconds=200)
#     result = time_hex_sec_subs(moment=moment, delta=delta)
#     print("integer part of unhex at moment + delta : %s " % result[0])
#     print("integer part of hexlify at moment + delta : %s " % binascii.hexlify(result[0]))
#     print("decimal part of unhex at moment + delta : %s " % result[1])
#     print("decimal part of hexlify at moment + delta : %s " % binascii.hexlify(result[1]))
#     print('====================================================================================================================')
#     now_result = time_hex_sec_subs(show_timestamp=True)
#     first = now_result[0]
#     second = now_result[1]
#     print("binascii.hexlify(integer part) at now : %s " % binascii.hexlify(first))
#     print("binascii.hexlify(decimal part ) at now : %s " % binascii.hexlify(second))
