# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/25 10:24
# @File    : test_002_lite_demo.py

import os
import pytest
from u2 import Element
from common.log import log
from u2.driver import Device
from u2.adb_command import ADB
from common.util import str_transform_dict
from common.exceptions import ElementNoFindException
from page.thinktool_lite_page import HomePage, DiagHomePage, InputMethodPage, CommandPage, LoginPage, SettingsPage


def test_001_lite(u2_driver: Device, pkg_name='com.us.thinktool'):
    """
    用户登录，诊断车型搜索，退出登录
    """
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

    # 进入到诊断页面
    home_page.diag_button.click()

    # 滑动找到：演示btn
    # while not diag_home_page.car_demo_button.exists():
    #     u2_driver.swipe_direction(style='UP')
    if not diag_home_page.car_demo_button.exists():
        for i in range(10):
            u2_driver.swipe_direction(style='UP', print_defined='当前页面中不存在需要操作的元素')
            if diag_home_page.car_demo_button.exists():
                break
            if i == 9:
                log.error(f'执行循环滑动{i+1}次，未定位到操作元素')
                raise ElementNoFindException()

    # 操作流程：演示 - 诊断 - 演示 - 选择车型
    diag_home_page.car_demo_button.click()
    diag_home_page.diag_button.click()
    diag_home_page.demo_confirm_button.click()
    diag_home_page.wait(5)
    diag_home_page.Ford_list.click()
    diag_home_page.fast_test.click()
    diag_home_page.wait(20)

    success_dict = {}
    failure_dict = {}

    # 此处使用while循环中的元素当前页面一定不存在，直到满足检测数量后自动跳出循环
    while not diag_home_page.fast_test.exists():
        log.info('进入到：车型诊断检测项 - 检测流程')
        for i in range(5):  # 此处的range数量需要根据当前页面最多可显示的数量来决定
            scan_name_text_element = f'resourceId="com.us.thinktool:id/tv_systemname", instance={i}, describe="检测项_btn"'
            scan_statue_text_element = f'resourceId="com.us.thinktool:id/tv_systemstatus", instance={i}, describe="检测状态_btn"'
            scan_name_text_use = Element(**str_transform_dict(scan_name_text_element))
            scan_statue_text_use = Element(**str_transform_dict(scan_statue_text_element))
            scan_name_text = scan_name_text_use.get_text()  # 获取检测项名称
            scan_statue_text = scan_statue_text_use.get_text()  # 获取检测异常数量，其中正常为''
            if scan_statue_text != '':
                if scan_name_text in failure_dict.keys():
                    continue
                else:
                    failure_dict[scan_name_text] = scan_statue_text
            else:
                if scan_name_text in success_dict.keys():
                    continue
                else:
                    success_dict[scan_name_text] = scan_statue_text

            if len(success_dict) + len(failure_dict) >= 17:
                log.info("检测项长度17，跳出内循坏！")
                break

        if len(success_dict) + len(failure_dict) >= 17:
            log.info("检测项长度17，跳出外循坏！")
            break
        u2_driver.swipe_direction(style='UP')

    log.info('检测成功项目：' + str(success_dict))
    log.warn('检测异常项目：' + str(failure_dict))

    # 生产检测PDF报告
    diag_home_page.report_button.click()
    # 此处的具体信息待添加
    diag_home_page.info_add_confirm.click()
    diag_home_page.more_info_confirm.click()
    diag_home_page.PDF_button.click()
    diag_home_page.wait(10)

    # 一直退出返回到首页
    i = 0
    while i < 5:
        common_page.wait(1)
        common_page.back_button.click()
        i += 1

    diag_home_page.quit_tips_confirm_button.click()
    # diag_home_page.quit_tips_confirm_button.click()
    diag_home_page.takeout_tips_confirm_button.click()

    # 输入查询指定车型，并弹出输入法弹窗
    # diag_home_page.search_button.click()
    # diag_home_page.search_input.click()
    # diag_home_page.wait(1)
    # diag_home_page.search_input.set_text('123333')
    # # adb.adb_input_text('baic')
    # diag_home_page.wait(1)
    # ime_page.delete_button.click()
    # ime_page.finish_button.click()

    # common_page.back_button.click()
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
