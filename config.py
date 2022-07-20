# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/6/30 20:02
# @File    : config.py

# 是否开启print打印
print_log = False


class Browser:
    """
    此方法适用于selenium方法
    """
    # 默认浏览器驱动
    driver = None

    # 是否对操作的操作元素添加边框
    show = True
