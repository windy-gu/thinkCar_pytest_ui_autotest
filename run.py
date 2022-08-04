# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/11 19:43
# @File    : run.py

import os
import time
import pytest
import click
from conftest import REPORT_DIR
# from common.logging import log
from common.log import log
from common.util import change_html
from conftest import cases_path, rerun, max_fail

'''
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python3 run.py  (回归模式，生成HTML报告)
  > python3 run.py -m debug  (调试模式)
'''


def init_report_path(report_file_dir: str):
    """
    初始化测试报告目录
    :param report_file_dir:
    :return:
    """
    # 生成测试报告xml和html的日志目录
    os.makedirs(os.path.join(REPORT_DIR, report_file_dir))

    # 生成测试截图目录
    os.makedirs(os.path.join(REPORT_DIR, report_file_dir, "image"))


@click.command()
@click.option('-m', default=None, help='Input run model：run or debug')
def run(m):
    # 测试的主测试入口
    if m is None or m == 'run':
        log.info("回归模式，开始执行！")
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        init_report_path(now_time)
        html_report = os.path.join(REPORT_DIR, now_time, "report.html")
        target_html_report = os.path.join(REPORT_DIR, now_time, "ui_report.html")
        xml_report = os.path.join(REPORT_DIR, now_time, "junit-xml.xml")
        pytest.main([
                    # "-s",  # 运行时显示详细信息
                    "-v",  # 显示打印消息
                    cases_path,  # 测试用例目录路径
                    "--html=" + html_report,  # 生成报告，此报告中css是独立的，分享时会丢失样式，pip3 install pytest-html
                    # "--junit-xml=" + xml_report,  # 生成xml报告文件
                    "--self-contained-html",  # 除了passed所有行都被展开
                    "--maxfail", max_fail,  # 遇到最大错误数就停止运行
                    "--reruns", rerun  # 失败重试次数，pip3 install pytest-rerunfailures
                    ])
        log.info("运行结束，生成测试报告！")
        change_html(html_report, target_html_report)  # 修改html中存在的异常代码，并删除旧文件

    elif m == "debug":
        # debug模式下，不生成HTML报告
        log.info("debug模式，开始执行！")
        pytest.main(["-v", "-s", cases_path])
        log.info("运行结束！")


if __name__ == '__main__':
    run()
