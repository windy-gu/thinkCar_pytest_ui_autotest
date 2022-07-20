# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/8 14:00
# @File    : page.py

from driver import Device


class Page:
    package_name = None
    activity_name = None
    url = None

    def __init__(self):
        self.initialized = False
        self.device: Device = None

    def __get__(self, instance, owner):
        if not self.initialized:
            if instance is None:
                raise Exception("持续类没有实例化")
