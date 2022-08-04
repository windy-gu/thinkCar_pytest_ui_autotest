# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/4 17:16
# @File    : __init__.py.py
import os
import sys
import time
from settings import Setting
from common.log import log
from common.assert_des import insert_assert
from common.exceptions import AssertNoEqualException


# u2定位支持类型
LOCATOR_LIST = [
    "text",
    "textContains",
    "textMatches",
    "textStartsWith",
    "className",
    "classNameMatches",
    "description",
    "descriptionContains",
    "descriptionMatches",
    "descriptionStartsWith",
    "checkable",
    "checked",
    "clickable",
    "longClickable",
    "scrollable",
    "enabled",
    "focusable",
    "focused",
    "selected",
    "packageName",
    "packageNameMatches",
    "resourceId",
    "resourceIdMatches",
    "index",
    "instance",
    "xpath",
]

current_path = os.path.abspath(__file__)
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")


class Page(object):
    """
    所有element-page的父类，需要在实例化的时候传入u2_driver
    """
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def wait(sleep_time_s: int = 1):
        """
        系统执行等待时间，单位：秒
        :param sleep_time_s:  默认值1，单位：秒
        """
        time.sleep(sleep_time_s)
        log.info(f'页面等待：{sleep_time_s} s')

    def window_size(self):
        """
        获取手机设备size值
        :return: 
        """
        return self.driver.window_size()

    def app_info(self, pkg_name=Setting.apk_name):
        """
        获取app相关信息参数

        Args:
            pkg_name (str): package name

        Return example:
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }

        Raises:
            UiaError
        """
        return self.driver.app_info(pkg_name)

    def click(self, x: float = None, y: float = None, text: str = None, screenshots=Setting.click_screenshots):
        """
        元素click操作
        :param x:
        :param y:
        :param text:
        :param screenshots:
        :return:
        """
        if not x and not y and not text:
            raise ValueError
        # (x, y) = self.driver(text=text).center() if text else (x, y) ==> 等价于如下if else流程
        if text:
            (x, y) = self.driver(text=text).center()
        else:
            (x, y) = (x, y)
        if screenshots:
            self.screenshots(x, y, describe="点击")
        else:
            self.screenshots(print("\n"), log.info(msg=" 点击 ==> " + "点击坐标{},{}".format(x, y)))
        self.driver.click(x, y)

    def screenshots(self, w=None, h=None, describe=None):
        """
        截图 -- todo
        :return:
        """
        if w and h:
            if w < 1 and h < 1:
                x, y = self.window_size()
                w, h = x * w, y * h

        ...

    def assert_text_exists(self, text: str, describe: str, sleep=0, timeout=10):
        """
        断言文案是否存在
        :param text:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)
        text_exists = self.driver(text=text).exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果：" + describe + " 文案存在")
        if text_exists is True:
            insert_assert(describe, True)
            log.info("实际结果：" + describe + " 文案存在")
        else:
            insert_assert(describe, False)
            log.warn("实际结果：" + describe + " 文案不存在")

    def assert_text_not_exists(self, text, describe, sleep=0, timeout=10):
        """
        断言文案是否不存在
        :param text:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)

        text_exists = self.driver(text=text).exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果: " + describe + " 文案不存在")
        if text_exists is True:
            insert_assert(describe, False)
            log.warn("实际结果: " + describe + " 文案存在")
        else:
            insert_assert(describe, True)
            log.info("实际结果: " + describe + " 文案不存在")

    def assert_element_exists(self, element, describe, sleep=0, timeout=10):
        """
        断言元素是否存在
        :param element:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)
        element_exists = element.exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果：" + describe + " 元素存在")
        if element_exists is True:
            insert_assert(describe, True)
            log.info("实际结果：" + describe + " 元素存在")
        else:
            insert_assert(describe, False)
            log.warn("实际结果：" + describe + " 元素不存在")

    def assert_element_not_exists(self, element, describe, sleep=0, timeout=10):
        """
        断言元素是否不存在
        :param element:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)

        element_exists = element.exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果: " + describe + " 元素不存在")
        if element_exists is True:
            insert_assert(describe, False)
            log.warn("实际结果: " + describe + " 元素存在")
        else:
            insert_assert(describe, True)
            log.info("实际结果: " + describe + " 元素不存在")

    def assert_contain_text(self, text, describe, sleep=0, timeout=10):
        """
        断言文案是否包含
        :param text:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)
        text_exists = self.driver(textContains=text).exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果：" + describe + " 文案存在")
        if text_exists is True:
            result = [describe, True]
            Setting.assert_result.append(result)
            log.info("实际结果：" + describe + " 文案存在")
        else:
            result = [describe, False]
            Setting.assert_result.append(result)
            log.warn("实际结果：" + describe + " 文案不存在")

    def assert_not_contain_text(self, text, describe, sleep=0, timeout=10):
        """
        断言文案是否不包含
        :param text:
        :param describe:
        :param sleep:       等待时间，默认0s
        :param timeout:     最大等待时间
        :return:
        """
        time.sleep(sleep)

        text_exists = self.driver(textContains=text).exists(timeout)
        self.screenshots(describe="断言")
        log.info("预期结果: " + describe + " 文案不存在")
        if text_exists is True:
            result = [describe, False]
            Setting.assert_result.append(result)
            log.info("实际结果：" + describe + " 文案存在")
        else:
            result = [describe, True]
            Setting.assert_result.append(result)
            log.warn("实际结果：" + describe + " 文案不存在")

    @staticmethod
    def assert_text_equals(text_1, text_2, describe):
        """
        断言文案相等
        :param text_1:
        :param text_2:
        :param describe:
        :return:
        """
        log.info("预期结果: " + text_1 + "," + text_2 + " 相等")
        if text_1 == text_2:
            result = [describe, True]
            Setting.assert_result.append(result)
            log.info("实际结果: " + text_1 + "," + text_2 + " 相等")
        else:
            result = [describe, False]
            Setting.assert_result.append(result)
            log.warn("实际结果: " + text_1 + "," + text_2 + " 不相等")
            raise AssertNoEqualException("实际结果: " + text_1 + "," + text_2 + " 不相等")

    @staticmethod
    def assert_text_not_equals(text_1, text_2, describe):
        """
        断言文案不相等
        :param text_1:
        :param text_2:
        :param describe:
        :return:
        """
        log.info("预期结果: " + text_1 + "," + text_2 + " 不相等")
        if text_1 == text_2:
            result = [describe, False]
            Setting.assert_result.append(result)
            log.warn("实际结果: " + text_1 + "," + text_2 + " 相等")
        else:
            result = [describe, True]
            Setting.assert_result.append(result)
            log.info("实际结果: " + text_1 + "," + text_2 + " 不相等")


class XpathElement(object):
    """
        Only CSS selectors are supported. | xpath方式实现的定位的父类
        https://github.com/openatx/uiautomator2/blob/master/XPATH.md

        >> from sabre import Page, XpathElement
        >> class MyPage(Page):
                input = XpathElement('//android.widget.EditText')
                button = XpathElement('@com.taobao.taobao:id/fl_banner_container')
        """

    driver = None

    def __init__(self, xpath, index=None, timeout=10, describe=None):
        self.xpath = xpath
        self.describe = describe
        if index is None:
            self.index = 0
        else:
            self.index = int(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def click(self, screenshots=Setting.click_screenshots):
        """
        Click element.
        """
        self.screenshots(describe="点击") if screenshots else (log.info(msg="点击 ==> " + self.describe), print("\n"))

        driver.xpath(self.xpath).click()
        if self.describe is not None:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k='xpath',
                            v=self.xpath,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k='xpath',
                            v=self.xpath,
                            method_name=sys._getframe().f_code.co_name))


    def set_text(self, value):
        """
        Simulates typing into the element.
        :param value: input text
        """
        default_ime = self.get_default_ime()
        driver.xpath(self.xpath).set_text(value)
        if self.describe is not None:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k='xpath',
                            v=self.xpath,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k='xpath',
                            v=self.xpath,
                            method_name=sys._getframe().f_code.co_name))

        change_ime = self.get_default_ime()
        if default_ime != change_ime:
            os.popen(Setting.adb_path + ' shell ime set' + default_ime)
            log.info(f"切换回原先设备的默认ime：{default_ime}")

    def get_text(self):
        """
        :return: get text from field
        """
        return driver.xpath(self.xpath).get_text()

    def match(self):
        """
        :return: None or matched XPathElement
        """
        return driver.xpath(self.xpath).match()

    def get_default_ime(self):
        default_ime = os.popen(Setting.adb_path + " shell settings get secure default_input_method").read()
        log.info(f'当前设备默认输入法：{default_ime}')
        return default_ime

    # def screenshots(self, describe=None):
    #     """
    #     截图，在对应元素上增加水印
    #     """
    #     global driver
    #     text = driver.xpath(self.xpath).get_text()
    #     if text == "":
    #         w, h = None, None
    #     else:
    #         w, h = driver(text=text).center()
    #     screenshots_dir = screenshots_name(describe)
    #     driver.screenshot(screenshots_dir)
    #     processing(screenshots_dir, w, h)
    # pass


class Element(object):
    driver = None

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.describe = describe
        self.time_out = timeout
        if describe is None:
            self.describe = "None"
        if not kwargs:
            raise ValueError("Please specify a locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST:
            raise KeyError("Element positioning of type '{}' is not supported".format(self.k))

    def __get__(self, instance, value):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def click(self, timeout=10, offset=None, screenshots=Setting.click_screenshots):
        """
        点击UI element
        :param timeout:     超时时间
        :param offset:      (xoff, yoff) default (0.5, 0.5) -> center
        :param screenshots:
        :return:
        """
        global driver
        driver(**self.kwargs).click(timeout, offset)
        if self.describe is None:

            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))

    def click_exists(self, timeout=1) -> bool:
        """
        元素存在则点击该元素，最多等待时间timeout，超时后元素未存在则抛异常
        """

        global driver
        return driver(**self.kwargs).click_exists(timeout=timeout)

    def click_gone(self) -> bool:
        """
        进行点击操作，当前点击元素不在当前页面，则return True，否则return False
        """

        global driver
        return driver(**self.kwargs).click_gone()

    def click_more(self, sleep=.01, times=3):
        """
        连续点击
        sleep(float): 间隔时间
        times(int): 点击次数
        """
        global driver
        x, y = self.center()
        for i in range(times):
            driver.touch.down(x, y)
            time.sleep(sleep)
            driver.touch.up(x, y)

    def exists(self, timeout=1):
        """
        check if the object exists in current window.
        """

        global driver
        return driver(**self.kwargs).exists(timeout=timeout)

    def not_exists(self, timeout=0):
        """
        check if the object exists in current window.
        """

        global driver
        return not driver(**self.kwargs).exists(timeout=timeout)

    def set_text(self, text):
        """
        input text
        :param text:
        """
        global driver
        driver(**self.kwargs).set_text(text=text)
        log.info(message="键盘输入 ==> " + text)

        if self.describe is None:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))

    def send_keys(self, text, clear=True):
        """
        alias of set_text | 清除文本&重新赋值
        :param text:
        :param clear:
        """
        global driver
        driver(**self.kwargs).click()
        driver.send_keys(text=text, clear=clear)

        if self.describe is not None:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name))

    def clear_text(self):
        """
        Clear the text | 清除元素文本内容
        """
        global driver
        driver(**self.kwargs).clear()
        if self.describe is not None:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))
        else:
            log.info("操作类型：{method_name} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k=self.k,
                            v=self.v,
                            method_name=sys._getframe().f_code.co_name))

    def get_text(self):
        """
        get element text | 获取元素文本内容
        """
        global driver
        get_text = driver(**self.kwargs).get_text()
        if self.describe is not None:
            log.info("操作类型：{method_name}，获取元素文本内容：{get_text} [ 定位_type：{k}， 定位_value：{v}， 描述：{describe} ]".
                     format(k=self.k,
                            v=self.v,
                            get_text=get_text,
                            method_name=sys._getframe().f_code.co_name,
                            describe=self.describe))
        else:
            log.info("操作类型：{method_name}，获取元素文本内容：{get_text} [ 定位_type：{k}， 定位_value：{v} ]".
                     format(k=self.k,
                            v=self.v,
                            get_text=get_text,
                            method_name=sys._getframe().f_code.co_name))
        return get_text

    def bounds(self):
        """
        Returns the element coordinate position | 返回元素坐标位置
        :return: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        """
        global driver
        return driver(**self.kwargs).bounds()

    def get_position(self):
        """
        获取元素所在位置
        :return:
        """
        global driver
        h, w = driver.window_size()
        x, y = self.center()
        return round(x / h, 4), round(y / w, 4)

    def center(self):
        """
        Returns the center coordinates of the element | 返回元素的中心坐标
        return: center point (x, y)
        """
        global driver
        return driver(**self.kwargs).center()

