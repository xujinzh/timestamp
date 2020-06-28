import binascii


def count(content_list, identifier_list, sync_header):
    """
    从搜索头后开始寻找某些字段，并统计有多少该字段，同时返回整个包数
    :param content_list: 包字符串列表
    :param identifier_list: 待统计字段列表，标识符
    :param sync_header: 搜索头
    :return: 字典形式信息
    """
    stat_iden = {"package_number": len(content_list)}
    for identifier in identifier_list:
        stat_iden[identifier] = 0

    for identifier in identifier_list:
        coun = 0
        for content in content_list:
            position = binascii.hexlify(content).find(identifier, len(sync_header) - 1, 20)
            if position != -1:
                coun += 1
        stat_iden[identifier] = coun

    return stat_iden
