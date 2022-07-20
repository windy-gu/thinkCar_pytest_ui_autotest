# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/5 17:51
# @File    : assert_des.py

from settings import Setting


def insert_assert(describe: str, result: bool):
    """
    插入断言信息
    :param describe:    断言描述信息
    :param result:      断言结果
    :return:
    """
    result = [describe, bool(result)]
    Setting.assert_result.append(result)
