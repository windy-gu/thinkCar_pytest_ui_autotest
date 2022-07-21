# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/1 17:24
# @File    : test_001_u2_demo.py

import os
import uiautomator2 as u2

# from u2 import Page, Element, Setting
# from u2.driver import Device


# class TestPage(Page):
#     mine = Element(resourceId="com.us.thinkdiag.plus:id/iv_mine", describe="我的")
#     setting = Element(resourceId="com.us.thinkdiag.plus:id/bt_setting", describe="设置")
#     pass


if __name__ == '__main__':
    d = u2.connect()
    print(d(resourceId="com.us.thinkdiag.plus:id/iv_mine").click_gone())
    print(d(resourceId="com.us.thinkdiag.plus:id/iv_mine").exists())
    # print(d(resourceId="com.us.thinkdiag.plus:id/iv_mine"))
    # driver = Device.connect()
    # # driver.screenshot()
    # pkg_name = 'com.us.thinkdiag.plus'
    # driver.unlock()
    #
    # print(driver.info)
    # driver.start_app(pkg_name)
    # driver.pull('./sdcard/screenshot_20220712165516.png', '/Users/gxf/Documents/thinkCarCode/ui/thinkCar_pytest_ui_web_autotest/test_report/2022_07_12_16_55_00/image/test_001_u2_demo.py_test_001_diag.png')
    # driver.adb_screencap_local()
    # # driver.sleep(5)
    # # driver.open_url('http://www.baidu.com')
    # page = TestPage(driver)
    # page.mine.click()
    # page.setting.click()


