# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/1 17:24
# @File    : test_001_u2_demo.py

import os
import pytest
from u2.driver import Device
from common.log import log
from page.temp_thinkcar_page import LoginPage, CommonPage


def test_001_diag(u2_driver: Device, pkg_name='com.us.thinkdiag.plus'):
    u2_driver.start_app(pkg_name)
    login_page = LoginPage(u2_driver)
    common_page = CommonPage(u2_driver)
    common_page.mine.click_gone()
    # page.setting.click()
    login_page.email_input.set_text('408563133@qq.com')
    login_page.wait(2)
    login_page.password_input.set_text('test123456')
    login_page.wait(2)
    if login_page.login_btn.exists():
        login_page.login_btn.click()
        if login_page.login_btn.click_gone():
            log.info('Login Successfully')
        else:
            raise Exception('有bug！')
    else:
        log.warn('元素不存在~~~~~')
    login_page.wait(2)


if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', '-v', './{}'.format(file_name)])
