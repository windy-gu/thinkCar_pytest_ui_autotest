# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/6/30 19:46
# @File    : ui_page_objects.py
import warnings
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from common import logging
from common.exceptions import FindElementTypesError
from common.exceptions import FindElementTimedOutException
import config
from config import Browser
from common.log import log
# from common.logging import log

# Map PageElement constructor arguments to webdriver locator enums

LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,

    # appium
    # 'ios_uiautomation': AppiumBy.IOS_UIAUTOMATION,
    # 'ios_predicate': AppiumBy.IOS_PREDICATE,
    # 'ios_class_chain': AppiumBy.IOS_CLASS_CHAIN,
    # 'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    # 'android_viewtag': AppiumBy.ANDROID_VIEWTAG,
    # 'android_data_matcher': AppiumBy.ANDROID_DATA_MATCHER,
    # 'android_view_matcher': AppiumBy.ANDROID_VIEW_MATCHER,
    # 'windows_uiautomation': AppiumBy.WINDOWS_UI_AUTOMATION,
    # 'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
    # 'image': AppiumBy.IMAGE,
    # 'custom': AppiumBy.CUSTOM,
}


class PageObject(object):
    """
    Page Object Pattern 页面设计模式
    """
    def __init__(self, driver, url=None, print_log: bool = False):
        """
        :param driver:      `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url:         `str`
        :param print_log:   `bool`
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)
        config.print_log = print_log

    def get(self, uri):
        warnings.warn("use page.open() instead",  # 弃用警告
                      DeprecationWarning, stacklevel=2)
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(8)  # 设置隐式等待时间8s，如果超出了设置的时长元素还没有被加载，则抛出NoSuchElementException

    def open(self, uri):
        """
        :param uri:
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(8)  # 设置隐式等待时间8s，如果超出了设置的时长元素还没有被加载，则抛出NoSuchElementException


class Element(object):
    """
    Returns an element object 返回元素类型
    """
    def __init__(self, timeout: int = 5, describe: str = "", index: int = 0, **kwargs):
        self.times = timeout
        self.index = index
        self.desc = describe
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):
        if instance is None:
            return None

        Browser.driver = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)

    def __elements(self, key, value):
        elements = Browser.driver.find_elements(key, value)
        return elements

    def __find_element(self, elem):
        """
        Find if the element exits.
        :param elem:
        :return:
        """
        for i in range(self.times):
            try:
                elems = self.__elements(elem[0], elem[1])
            except FindElementTimedOutException:
                elems = []

            if len(elems) == 1:
                log.info(f"🔍 Find element: {elem[0]}={elem[1]}. {self.desc}")
                break
