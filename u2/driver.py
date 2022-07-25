# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/4 17:16
# @File    : driver.py

import os
import time
import uiautomator2 as u2
from settings import Setting
from common.log import log
from u2.adb_command import ADB


class Device(u2.Device):
    """
    Android设备类，封装uiautomator2的Device类
    """

    def __init__(self, u2d: u2.Device):
        # 把u2.Device的属性字典复制过来
        self.__dict__ = u2d.__dict__

    @staticmethod
    def connect():
        """
        Driver connect 设备连接
        :return:
        """
        if Setting.connect_usb:
            if Setting.device_id == '':
                device_id = get_device_id()
                Setting.device_id = device_id

            d = u2.connect_usb(Setting.device_id)
            log.info(f'连接设备:[ {Setting.device_id} ]')
            log.info(f'设备信息:[ {d.info} ]')
            return Device(d)

    def sleep(self, seconds: float = 1):
        """
        等待时间
        :param seconds:
        :return:
        """
        log.info(f'等待 {seconds}s')
        time.sleep(seconds)

    def adb_shell(self, command: str):
        """
        执行adb_shell命令
        :param command:
        :return:
        """
        log.info(f'执行adb命令：[ {command} ]')
        output, exit_code = self.shell(command)
        log.info(f'{Setting.adb_path} shell output:\n {output}')
        log.info(f'{Setting.adb_path} shell exitCode:[ {exit_code} ]')

    def start_app(self, package_name, activity=None):
        """
        启动app
        :param package_name:
        :param activity:
        :return:
        """
        log.info(f'启动App：[ {package_name} ]')
        self.app_start(package_name, activity)
        self.sleep(3)

    def app_restart(self, package_name, activity=None):
        """
        重启app
        :param package_name:
        :param activity:
        :return:
        """
        log.info(f'重启App：[ {package_name} ]')
        self.app_stop(package_name)
        self.app_start(package_name, activity)
        self.app_wait(package_name)

    def save_app_icon(self, package_name, path):
        """
        保存App图标
        :param package_name:
        :param path:
        :return:
        """
        log.info(f'保存App图标：[ {package_name} ] 存放路径：[ {path} ]')
        icon = self.app_icon(package_name)
        icon.save(path)

    def fastinput_ime(self, text: str):
        """
        通过切换到FastInputIME输入法，文本输入，输入完切换回最初的输入法
        :param text:
        :return:
        """
        log.info('切换为FastInputIME输入法')
        self.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        self.sleep(0.5)
        log.info(f'输入:[ {text} ]')
        self.send_keys(text)  # adb广播输入
        self.sleep(0.5)
        self.set_fastinput_ime(False)  # 切换成正常的输入法
        log.info('切换为正常的输入法')

    def get_toast_message(self, wait_timeout=10, cache_timeout=10, default=None):
        """
        获取toast信息内容
        :param wait_timeout:
        :param cache_timeout:
        :param default:
        :return:
        """
        log.info('获取toast信息')
        toast_msg = self.toast.get_message(wait_timeout, cache_timeout, default)
        log.info(f'toast:[ {toast_msg} ]')
        return toast_msg

    def swipe_up_to_unlock_device(self, style: str = 'UP'):
        """
        通过向上滑动解锁
        :return:
        """
        width, height = ADB().adb_get_screen_size().split('x')
        width = width.replace('\n', '')
        x_height = 0.2 * int(height)
        x_width = 0.5 * int(width)
        y_height = 0.8 * int(height)
        y_width = 0.5 * int(width)
        if style == 'UP':
            self.swipe(y_width, y_height, x_width, x_height)
        elif style == 'DOWN':
            self.swipe(x_width, x_height, y_width, y_height, )


def get_device_id():
    """
    获取设备的 device ID
    :return:
    """
    status_code = os.system(Setting.adb_path + " devices")
    if status_code != 0:
        raise SystemError("Verify that adb is properly installed and started | 检查adb是否正确安装并启动")

    # 获取当前已连接电脑的移动设备serialNo & 设备状态：device & 取第一行数据
    temp_list = os.popen(Setting.adb_path + " devices | grep -w 'device' | head -1 ")
    device = temp_list.read()

    if device == '':
        raise NameError("Unavailable device | 无可用设备")
    else:
        device_id = device.split("\t")[0]

        return device_id


def start_app(driver, apk=None):
    """
    启动APP
    :param driver:  u2驱动
    :param apk:     package_name
    :return:
    """
    if apk is None:
        apk = Setting.apk_name
    driver.app_start(apk, use_monkey=True)
    # 等待应用前台运行，最长等待时间20s（默认），settings设置超时时间10s
    driver.app_wait(apk, front=True, timeout=Setting.app_wait)
    driver.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})

    session = driver.session(apk, attach=True)
    session.implicitly_wait(Setting.implicitly_wait)
    return session


def close_app(driver, apk=None):
    """
    关闭APP
    :param driver:
    :param apk:
    :return:
    """
    if apk is not None:
        driver.app_stop(apk)
    else:
        driver.app_stop(Setting.apk_name)


if __name__ == '__main__':
    # status_code = os.system(Setting.adb_path + " devices")
    # print(status_code)
    execute_result = os.popen(Setting.adb_path + " shell dumpsys window policy | grep isStatusBarKeyguard").read().split('=')[-1]
    # execute_result = os.popen(Setting.adb_path + " shell wm size").read().replace(' ', '').split(':')[-1]
    print(execute_result)
    # w, h = execute_result.split('x')
    # print(w, h)
