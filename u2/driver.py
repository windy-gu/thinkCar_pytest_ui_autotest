# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/4 17:16
# @File    : driver.py

import os
import time
import uiautomator2 as u2
from settings import Setting
# from common.logging import log
from common.log import log
from adb_command import ADB
from datetime import datetime


class Device(u2.Device, ADB):
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

    @staticmethod
    def check_apk_exits(pkg_name: str) -> bool:
        """
        检查apk应用是否在当前设备应用列表中
        :param pkg_name:
        :return:
        """
        apk_check_str = os.popen(Setting.adb_path + ' shell pm list packages ' + pkg_name).read()
        if pkg_name in apk_check_str:
            log.info(f'当前设备存在应用：{pkg_name}')
            return True
        else:
            log.warn(f'当前设备不存在应用：{pkg_name}')
            return False

    def check_screen_status(self) -> bool:
        """
        检查手机屏幕亮屏状态,ON亮屏/OFF息屏
        :return:  bool Ture亮屏/False息屏
        """
        status = os.popen(Setting.adb_path + " shell dumpsys power | grep 'Display Power'").read().split('=')[-1].replace('\n', '')
        log.info(f'{status}')
        if status == 'ON':
            log.info(f'当前设备屏幕状态：亮屏')
            return True
        else:
            log.info(f'当前设备屏幕状态：息屏')
            return False

    def check_screen_lock_status(self) -> bool:
        """
        检查手机屏幕锁屏状态,true 锁屏状态/false 非锁屏
        :return:  bool Ture锁屏/False非锁屏
        """
        status = os.popen(Setting.adb_path + " shell dumpsys window policy | grep isStatusBarKeyguard").read().split('=')[-1].replace('\n', '')
        if status == 'true':
            log.info('当前设备屏幕锁屏状态：锁屏')
            return True
        else:
            log.info('当前设备屏幕锁屏状态：非锁屏')
            return False

    def wake_up_screen(self):
        """
        唤醒/关闭屏幕
        :return:
        """
        os.popen(Setting.adb_path + " shell input keyevent 26")

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

    def open_url(self, url: str):
        """
        通过Android内置参数，根据内容打开相应的Activity
        url -- 浏览器
        tel:13800138000 -- 拨号程序
        geo:38.383838,126.126126 -- 打开地图定位
        :param url:
        :return:
        """
        self.adb_shell(f'am start -a android.intent.action.VIEW -d "{url}"')

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

    def adb_input(self, text: str):
        """
        通过adb shell input text 进行内容输入，不限于字母、数字、汉字等
        :param text:    输入文本内容
        :return:
        """
        self.adb_shell(f'input text [ {text} ]')

    def adb_refresh_gallery(self, file_uri: str) -> None:
        """
        上传图片至系统图库后，手动广播通知系统图库刷新
        :param file_uri:
        """
        log.info('ADB广播刷新系统图库')
        if file_uri.startswith('/'):
            file_uri = file_uri[1:]
        self.adb_shell(
            fr'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{file_uri}')

    @staticmethod
    def adb_screencap_local(project_image_path: str = None, path: str = None) -> None:
        """
        设备本地截图
        :param path:
        :return:
        """
        if not path:
            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'screenshot_{current_time}.png'
            path = f'./sdcard/{filename}'
        if Setting.device_id == '':
            # log.info("无device_id模式")
            # 直接将截图保存在当前工程目录test_report/time/image目录下
            os.popen(Setting.adb_path + f' shell screencap -p > {project_image_path}')
            time.sleep(2)
            log.info(f'异常截图已保存，文件路径：{project_image_path}')
        else:
            # log.info("device_id模式")
            # log.info(Setting.adb_path + ' -s ' + Setting.device_id + f' shell screencap {path}')
            os.popen(Setting.adb_path + ' -s ' + Setting.device_id + f' shell screencap -p > {project_image_path}')
            time.sleep(2)
            log.info(f'异常截图已保存在：{project_image_path}')

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

    def get_screen_size(self) -> str:
        """
        获取屏幕尺寸大小Size:720x1600
        :return:
        """
        return os.popen(Setting.adb_path + " shell wm size").read().replace(' ', '').split(':')[-1]

    def swipe_up_to_unlock_device(self):
        """
        通过向上滑动解锁
        :return:
        """
        width, height = self.get_screen_size().split('x')
        # log.info(type(width))
        # log.info(type(height))
        width_x1 = int(width)*0.5
        width_y1 = int(height)*0.7
        width_x2 = int(width)*0.5
        width_y2 = int(height)*0.7
        self.swipe_points([(width_x1, width_y1), (width_x2, width_y2)], 1)
        # self.swipe_ext('up', scale=0.8)


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
