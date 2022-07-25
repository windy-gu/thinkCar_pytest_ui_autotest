# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/25 09:53
# @File    : thinktool_lite_page.py

from u2 import Page, Element, XpathElement


class HomePage(Page):
    diag_button = Element(resourceId='com.us.thinktool:id/tv_entrance_bottom_name', describe='诊断_btn')
    maintenance_service_button = XpathElement('//*[@resource-id="com.us.thinktool:id/container"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]', describe='保养服务_btn')
    fast_detect_button = XpathElement('//*[@resource-id="com.us.thinktool:id/container"]/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]', describe='快速检测_btn')
    thinkcar_mall_button = XpathElement('//*[@resource-id="com.us.thinktool:id/container"]/android.widget.LinearLayout[4]/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]', describe='星卡商城_btn')
    thinkcar_model_button = Element(resourceId='com.us.thinktool:id/ll_entrance_bottom_container', describe='星卡模组_btn')
    upgrade_software_button = Element(resourceId="	com.us.thinktool:id/iv_upgrade", describe="更新_btn")
    file_report_button = Element(resourceId="com.us.thinktool:id/iv_file", describe='文件报告_btn')
    setting_btn = Element(resourceId="com.us.thinktool:id/iv_setting", describe='设置_btn')


class DiagHomePage(Page):
    search_button = Element(resourceId='com.us.thinktool:id/ts_fragment_quit', describe='搜索_btn')
    search_input = Element(resourceId='com.us.thinktool:id/searchView', describe='搜索_input')


class InputMethodPage(Page):
    finish_button = Element(description='完成', describe='输入法-完成_btn')
    continue_button = Element(description='繼續', describe='输入法-繼續_btn')
    delete_button = Element(description='刪除', describe='输入法-删除_btn')


class LoginPage(Page):
    email_input = Element(resourceId='com.us.thinktool:id/et_complete_input', describe='邮箱_input')
    email_clear_button = Element(resourceId='com.us.thinktool:id/iv_clear', describe='邮箱clear_btn')
    password_input = Element(resourceId='com.us.thinktool:id/et_login_password', describe='密码_input')
    forget_password_button = Element(resourceId='com.us.thinktool:id/tv_forget_password', describe='忘记密码_btn')
    login_button = Element(resourceId="com.us.thinktool:id/right_button_text", text="登錄", describe='登錄_btn')
    create_user_button = Element(resourceId="com.us.thinktool:id/right_button_text", text="創建帳戶", describe='創建帳戶_btn')
    network_settings_button = Element(resourceId="com.us.thinktool:id/right_button_text", text="網絡設置", describe='網絡設置_btn')
    free_trial_button = Element(resourceId="com.us.thinktool:id/right_button_text", textContains="免費試用", describe='免費試用_btn')
    delete_button = Element(description='刪除', describe='输入法-删除_btn')


class SettingsPage(Page):
    logout_button = Element(resourceId="com.us.thinktool:id/tv_left_text", text="退出登錄", describe='退出登錄_btn')
    logout_cancel = Element(resourceId="com.us.thinktool:id/button2", describe='登出取消_btn')
    logout_confirm = Element(resourceId="com.us.thinktool:id/button1", describe='登出确定_btn')
    ...


class CommandPage(Page):
    back_button = Element(resourceId='com.us.thinktool:id/ts_fragment_back', describe='返回_btn')
