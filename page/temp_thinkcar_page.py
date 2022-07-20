# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/12 15:24
# @File    : temp_thinkcar_page.py

from u2 import Page, Element, Setting, XpathElement
from u2.driver import Device


class DiagAndroidPage(Page):
    setting = Element(resourceId="com.us.thinkdiag.plus:id/bt_setting", describe="设置")


class LoginPage(Page):
    email_input = XpathElement('//*[@resource-id="com.us.thinkdiag.plus:id/overscroll"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]', describe='邮箱_input')
    password_input = XpathElement('//*[@resource-id="com.us.thinkdiag.plus:id/ll_psd_container"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]', describe='密码_input')
    email_clear = Element(resourceId="com.us.thinkdiag.plus:id/iv_clear", describe="email_清除")
    sign_up_btn = Element(resourceId="com.us.thinkdiag.plus:id/tv_regist", describe='注册_btn')
    forgot_password_btn = Element(resourceId="com.us.thinkdiag.plus:id/tv_forget_password", describe='忘记密码_btn')
    login_btn = Element(resourceId="com.us.thinkdiag.plus:id/bt_login_login", describe='登录_btn')


class CommonPage(Page):
    top_close_btn = Element(resourceId="com.us.thinkdiag.plus:id/iv_top_close", describe='右上角_close_btn')
    mine = Element(resourceId="com.us.thinkdiag.plus:id/iv_mine", describe="我的")

