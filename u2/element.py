# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/8 14:02
# @File    : element.py
from functools import wraps
from uiautomator2 import UiObject
from driver import Device
from time import sleep
from common.logging import log
from common.log import log
from common.exceptions import ElementException
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError


class Locator(dict):
    ...


def retry_find_u2element(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay = kwargs.pop('timeout', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('timeout', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            sleep(delay)
        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'retry find element timeout',
                        'data': str(element.selector)
                    },
                    method='retry_find_u2element')

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(interval)
            element = func(*args, **kwargs)
            if element.exists:
                return Element(ui_object=element)
        raise UiObjectNotFoundError(
            {
                'code': -32002,
                'message': 'retry find element timeout',
                'data': str(element.selector)
            },
            method='retry_find_u2element')
    return wrapper


class Element(UiObject):
    def __init__(self,
                 ui_object: UiObject = None,
                 delay: float = 0.5,
                 timeout: float = 10,
                 interval: float = 0.5,
                 **kwargs):
        if ui_object:
            # 直接把UiObject的属性字典复制过来
            self.__dict__.update(ui_object.__dict__)
        self.delay = delay
        self.timeout = timeout
        self.interval = interval
        self.kwargs = kwargs

    def __retry_find(self, device: Device):
        # 计算重试次数
        retry_count = int(float(self.timeout) / float(self.interval))

        # 延迟查找元素
        if self.delay:
            sleep(self.delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            element = device(**self.kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
            else:
                raise UiObjectNotFoundError(
                    {
                        'code': -32002,
                        'message': 'retry find element timeout',
                        'data': str(element.selector)
                    },
                    method='Element.__retry_find')

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            if i > 0:
                sleep(self.interval)
            element = device(**self.kwargs)
            if element.exists:
                self.__dict__.update(element.__dict__)
                return self
        raise UiObjectNotFoundError(
            {
                'code': -32002,
                'message': 'retry find element timeout',
                'data': str(element.selector)
            },
            method='Element.__retry_find')

    def scroll_to_child(self, **kwargs):
        """滚动查找元素"""
        if self.scroll.to(**kwargs):
            return self.child(**kwargs)
        else:
            raise UiObjectNotFoundError(
                {
                    'code': -32002,
                    'message': 'retry find element timeout',
                    'data': str(self.selector)
                },
                method='Element.scroll_to_child')

    @retry_find_u2element
    def child(self, **kwargs):
        return super().child(**kwargs)

    @retry_find_u2element
    def sibling(self, **kwargs):
        return super().sibling(**kwargs)

    @retry_find_u2element
    def right(self, **kwargs):
        return super().right(**kwargs)

    @retry_find_u2element
    def left(self, **kwargs):
        return super().left(**kwargs)

    @retry_find_u2element
    def up(self, **kwargs):
        return super().up(**kwargs)

    @retry_find_u2element
    def down(self, **kwargs):
        return super().down(**kwargs)

    def __getitem__(self, instance: int):
        return Element(ui_object=super().__getitem__(instance))

    def __get__(self, instance, owner):
        if instance is None:
            raise ElementException('持有类没有实例化')
        return self.__retry_find(instance.device)

    def __set__(self, instance, value):
        raise NotImplementedError('老老实实set_text()吧')
