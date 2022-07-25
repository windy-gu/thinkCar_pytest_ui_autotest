# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/25 10:24
# @File    : test_002_lite_demo.py

import os
import pytest
from u2.driver import Device
from u2.adb_command import ADB
from common.log import log
from page.thinktool_lite_page import HomePage, DiagHomePage, InputMethodPage, CommandPage, LoginPage, SettingsPage


def test_001_lite(u2_driver: Device, pkg_name='com.us.thinktool'):
    # 实例化页面相关参数
    u2_driver.start_app(pkg_name)
    home_page = HomePage(u2_driver)
    diag_home_page = DiagHomePage(u2_driver)
    ime_page = InputMethodPage(u2_driver)
    common_page = CommandPage(u2_driver)
    adb = ADB()

    # 判断当前用户是否已登录，未登录则进行登录操作
    login_page = LoginPage(u2_driver)
    if login_page.login_button.exists():
        login_user(u2_driver, login_email='408563133@qq.com', password='123456')

    home_page.diag_button.click()
    diag_home_page.search_button.click()
    diag_home_page.search_input.click()
    diag_home_page.wait(1)
    diag_home_page.search_input.set_text('123333')
    # adb.adb_input_text('baic')
    diag_home_page.wait(1)
    print(ime_page.finish_button.exists())
    ime_page.delete_button.click()
    ime_page.finish_button.click()
    common_page.back_button.click()
    diag_home_page.wait(1)
    common_page.back_button.click()

    # 进行登出操作流程
    if home_page.setting_btn.exists():
        logout_user(u2_driver)


def login_user(u2_driver: Device, login_email: str, password: str):
    """
    用户登录流程
    :param u2_driver:
    :param login_email:
    :param password:
    :return:
    """
    login_page = LoginPage(u2_driver)
    ime_page = InputMethodPage(u2_driver)
    log.info(f'当前设备未登录，进行登录操作。登录账号：{login_email}')
    login_page.email_input.set_text(login_email)
    ime_page.continue_button.click()
    login_page.password_input.set_text(password)
    ime_page.finish_button.click()
    if login_page.login_button.click_gone():
        log.info(f'账号：{login_email}, 登录成功')
    else:
        log.error(f'账号：{login_email}, 登录失败')
        raise Exception("出错了，详情看日志哈~~~~")


def logout_user(u2_driver: Device):
    """
    用户登出流程
    :param u2_driver:
    :return:
    """
    home_page = HomePage(u2_driver)
    common_page = CommandPage(u2_driver)
    settings_page = SettingsPage(u2_driver)
    home_page.setting_btn.click()
    if common_page.back_button.exists():
        log.info('进入到设置页面:成功')
        while not settings_page.logout_button.exists():
            u2_driver.swipe_direction(style='UP')

        settings_page.logout_button.click()
        if settings_page.logout_confirm.click_gone():
            log.info(f'账号登出成功')
        else:
            log.error(f'账号登出失败')
            raise Exception("出错了，详情看日志哈~~~~")
    else:
        log.error('进入到设置页面:失败，详细看截图和日志')


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', '-v', './{}'.format(file_name)])
