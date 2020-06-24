def convert_to_double_byte(str_hex):
    """
    毫秒和微妙太小，可能会导致亚秒对应的十六进制字符串不足两个字节(2B)，如字符串型十六进制数'0xab'对应的十六进制字符串b'ab'只有一个字节(一个
    字母在十六进制数中代表4个比特位，8个比特位为一个字节），需要考虑在前面补充'00'，填补成两个字节，成为'0x00ab'
    :param str_hex: 字符串型十六进制数。至少有一位有效位，即类似于'0x0'型
    :return: 填充成两个字节的字符串型十六进制数
    """
    if len(str_hex) == 6:  # 如果就是4个字节，除去'0x'，那么字节返回
        two_byte_str_hex = str_hex
    elif len(str_hex) == 5:  # 如果微秒为0，则补一个字符 '0'，变成 b'07bd'的形式
        two_byte_str_hex = str_hex[:2] + '0' + str_hex[2:]
    elif len(str_hex) == 4:  # 如果毫秒和微秒设置太小，则补 '00'，变成 b'007b'的形式
        two_byte_str_hex = str_hex[:2] + '00' + str_hex[2:]
    else:  # 如果毫秒和微秒设置太小，则补 '000'，变成 b'0007'的形式。
        two_byte_str_hex = str_hex[:2] + '000' + str_hex[2:]

    return two_byte_str_hex


if __name__ == "__main__":
    for str in ['0x0', '0x10', '0x231', '0x234a']:
        str_hex_two_byte = convert_to_double_byte(str_hex=str)
        print(str_hex_two_byte)
