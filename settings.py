# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/4 17:17
# @File    : settings.py

import os
import datetime
import platform
current_path = os.path.abspath(__file__)  # 获取当前文件目录和文件名
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep)  # 获取当前文件目录所在路径




class Setting:

    # 是否通过usb链接设备
    connect_usb = True

    # 设备ID，deviceID，如果为空，则自动获取连接本地pc的第一个可用设备
    device_id = ""

    # 打开APP的包名
    apk_name = ""

    # 默认点击截图开关
    click_screenshots = True

    # 报告保存路径
    report_path = "."

    # 报告截图路径
    report_snapshot = "."

    # 断言结果
    assert_result = []

    # 打开APP等待启动时间
    app_wait = 10

    # 设置元素查找等待时间
    implicitly_wait = 10

    # 设置首页加载完成等待时间
    loading_finish = 10

    """
        返回到当前系统运行的系统，
        win系统 return windows
        mac系统 return Darwin
        linux系统 return linux
        """
    run_system = platform.system()
    if run_system == 'Darwin':
        # adb工程文件路径
        adb_path = BASE_DIR + '/adb_util/mac/adb'
        # aapt工程文件路径
        aapt_path = BASE_DIR + '/adb_util/mac/aapt'

    elif run_system == 'windows':
        # adb工程文件路径
        adb_path = BASE_DIR + '/adb_util/win/adb'
        # aapt工程文件路径
        aapt_path = BASE_DIR + '/adb_util/win/aapt'

    elif run_system == 'linux':
        # adb工程文件路径
        adb_path = BASE_DIR + '/adb_util/linux/adb'
        # aapt工程文件路径
        aapt_path = BASE_DIR + '/adb_util/linux/aapt'

    else:
        raise Exception('执行系统不在指定范围内')

    # 执行过程中image存放路径
    image_path = ''


if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
    # print(BASE_DIR)
    # print(current_path)
