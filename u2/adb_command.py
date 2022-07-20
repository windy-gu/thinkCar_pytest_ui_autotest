# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/20 13:56
# @File    : adb_command.py

import os
from common.log import log
from settings import Setting
import time


class ADB:
    """
    ADB 相关操作方法
    """
    def __init__(self):
        self.adb = Setting.adb_path

    def adb_shell(self, command: str):
        return os.popen(self.adb + ' shell ' + command)

    def adb_get_device(self):
        """
        获取设备的 device ID
        :return:
        """
        status_code = os.system(self.adb + " devices")
        if status_code != 0:
            raise SystemError("Verify that adb is properly installed and started | 检查adb是否正确安装并启动")

        # 获取当前已连接电脑的移动设备serialNo & 设备状态：device & 取第一行数据
        temp_list = os.popen(self.adb + " devices | grep -w 'device' | head -1 ")
        device = temp_list.read()

        if device == '':
            raise NameError("Unavailable device | 无可用设备")
        else:
            device_id = device.split("\t")[0]
            return device_id

    def adb_start_app(self, apk_name, activity = None, apk_path = None):
        """
        adb命令启动app应用
        :param apk_name:
        :return:
        """
        if apk_path is None:
            if activity is None:
                log.warn("未指定apk_path路径，请使用page.start_app()方法来启动应用")
            else:
                self.adb_shell('am start -n ' + apk_name + '/' + activity)
                log.info(f"adb命令 - 启动apk：{apk_name}")
        else:
            if activity is None:
                activity = AAPT().aapt_get_activity(apk_path=apk_path)
                if activity == '':
                    log.warn("activity为空，请使用page.start_app()方法来启动应用")
            else:
                self.adb_shell('am start -n ' + apk_name + '/' + activity)
                log.info(f"adb命令 - 启动apk：{apk_name}")

    def adb_stop_app(self, apk_name):
        """
        adb命令强制停止app进程
        :param apk_name:
        :return:
        """
        self.adb_shell('am force-stop ' + apk_name)
        log.info(f"adb命令 - 停止apk进程：{apk_name}")

    def adb_clear_app(self, apk_name):
        """
        adb命令清除app应用数据(同时也会结束app进程)
        :param apk_name:
        :return:
        """
        self.adb_shell('pm clear ' + apk_name)
        log.info(f"adb命令 - 清除apk数据：{apk_name}")

    def adb_check_apk_exits_device(self, apk_name):
        """
        adb命令判断app是否在当前连接设备中
        :param apk_name:
        :return:
        """
        apk_check_str = self.adb_shell('pm list packages ' + apk_name).read()
        if apk_name in apk_check_str:
            log.info(f'当前设备存在应用：{apk_name}')
            return True
        else:
            log.warn(f'当前设备不存在应用：{apk_name}')
            return False

    def adb_check_screen_status(self) -> bool:
        """
        检查手机屏幕亮屏状态,ON亮屏/OFF息屏
        :return:  bool Ture亮屏/False息屏
        """
        status = self.adb_shell("dumpsys power | grep 'Display Power'").read().split('=')[-1].replace('\n', '')
        # log.info(f'{status}')
        if status == 'ON':
            log.info(f'当前设备屏幕状态：亮屏')
            return True
        else:
            log.info(f'当前设备屏幕状态：息屏')
            return False

    def adb_check_screen_lock_status(self) -> bool:
        """
        检查手机屏幕锁屏状态,true 锁屏状态/false 非锁屏
        :return:  bool Ture锁屏/False非锁屏
        """
        status = self.adb_shell("dumpsys window policy | grep isStatusBarKeyguard").read().split('=')[-1].replace('\n', '')
        if status == 'true':
            log.info('当前设备屏幕锁屏状态：锁屏')
            return True
        else:
            log.info('当前设备屏幕锁屏状态：非锁屏')
            return False

    def adb_pull_file(self, device_file_path, computer_file_path):
        """
        将手机设备的文件，拉到指定电脑设备路径
        :param device_file_path:
        :param computer_file_path:
        :return:
        """
        os.popen(Setting.adb_path + ' pull {} {}'.format(device_file_path, computer_file_path))

    def adb_push_file(self, device_file_path, computer_file_path):
        """
        将指定电脑设备路径文件，拉到指定手机设备的路径
        :param device_file_path:
        :param computer_file_path:
        :return:
        """
        os.popen(Setting.adb_path + ' push {} {}'.format(computer_file_path, device_file_path))

    def adb_install_apk(self, apk_file_path):
        """
        通过adb install 命令安装apk应用
        :param apk_file_path:
        :return:
        """
        os.popen(Setting.adb_path + ' install -r {}'.format(apk_file_path))

    def adb_uninstall_apk(self, apk_name):
        """
        通过adb uninstall 命令卸载apk应用
        :param apk_name:
        :return:
        """
        os.popen(Setting.adb_path + ' uninstall {}'.format(apk_name))

    def adb_wake_up_screen(self):
        """
        唤醒/关闭屏幕
        :return:
        """
        self.adb_shell("input keyevent 26")
        # os.popen(Setting.adb_path + " shell input keyevent 26")


class AAPT:
    """
    AAPT 相关操作方法
    """
    def __init__(self):
        self.aapt = Setting.aapt_path

    def aapt_get_activity(self, apk_path: str) -> str:
        """
        aapt 获取指定路径apk的activity
        :param apk_path:
        :return:
        """
        activity_str = os.popen(self.aapt + ' dump badging ' + apk_path + ' | grep launchable-activity').read().split("name='")[-1].split("'  ")[0]
        return activity_str


if __name__ == '__main__':
    # aapt = AAPT()
    # aapt.aapt_get_activity('/Users/gxf/Downloads/Diag_7.1_2_debug\ \(1\).apk ')
    adb = ADB()
    adb.adb_clear_app('com.us.thinkdiag.plus')
    time.sleep(1)
    adb.adb_start_app('com.us.thinkdiag.plus', 'com.zhiyicx.thinksnsplus.modules.guide.GuideActivityNew')
    time.sleep(5)
    # adb.adb_stop_app('com.us.thinkdiag.plus')