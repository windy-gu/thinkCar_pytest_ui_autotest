# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/11 20:09
# @File    : conftest.py

import os
import pytest
from py.xml import html
from common.log import log
from settings import Setting
from u2.driver import Device
from u2.adb_command import ADB


# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"


############################

# 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
# driver_type = "chrome"

# 配置运行的 URL
# url = "https://www.baidu.com"

# 失败重跑次数
rerun = "0"

# 当达到最大失败数，停止执行
max_fail = "5"

# 运行测试用例的目录或文件
cases_path = "./test_dir/"

# 是否显示操作标注框
# browser_show = True

############################


# 设置用例描述表头
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


# 设置用例描述表格
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            screen_img_path = capture_screenshot(case_name)
            if screen_img_path is False:
                pass
            else:
                img_path = "/image/" + case_name.split("/")[-1]
                if os.path.exists(screen_img_path):  # 判断图片文件是否存在，存在则添加日志报告中
                    # 此处使用绝对路径获取图片文件
                    # html = '<div><img src="file://%s" alt="screenshot" style="width:304px;height:228px;" ' \
                    #        'onclick="window.open(this.src)" align="right"/></div>' % screen_img_path

                    # 此处使用相对路径获取图片文件
                    html = '<div><img src=".%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % img_path

                    extra.append(pytest_html.extras.html(html))
        report.extra = extra


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")
        ),
        html.body(
            [html.p(line) for line in desc_lines]
        )
    )
    return desc_html


def capture_screenshot(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    new_report_dir = new_report_time()
    if not new_report_dir:
        log.warn('没有初始化测试报告目录')
        return False
    else:
        image_path = os.path.join(REPORT_DIR, new_report_dir, "image")
        image_file_path = os.path.join(REPORT_DIR, new_report_dir, "image", file_name)
        if Setting.image_path == '':
            Setting.image_path = image_file_path
        if os.path.exists(image_path):
            ADB().adb_screencap_local(project_image_path=image_file_path)
        else:
            log.warn("report/image 路径不存在，取消截图操作")
        return image_file_path


def new_report_time():
    """
    获取最新报告的目录名（即运行时间，例如：2018_11_21_17_40_44）
    先判断当前是否存在报告目录，不存在则创建
    """
    is_report_path_exist = os.path.exists(REPORT_DIR)
    if is_report_path_exist is False:
        os.makedirs(REPORT_DIR)
    files = os.listdir(REPORT_DIR)
    if len(files) < 1:
        return False
    else:
        files.sort()
        try:
            return files[-1]
        except IndexError:
            return None


@pytest.fixture(scope='session', autouse=True)
def u2_driver():
    """
    设置全局u2 driver
    :return:
    """
    global driver
    driver = Device.connect()
    adb = ADB()
    if not adb.adb_check_screen_status():
        adb.adb_wake_up_screen()
        if adb.adb_check_screen_lock_status():
            Device(driver).swipe_direction(style='UP')
    else:
        if adb.adb_check_screen_lock_status():
            Device(driver).swipe_direction(style='UP')
        else:
            pass

    return driver
