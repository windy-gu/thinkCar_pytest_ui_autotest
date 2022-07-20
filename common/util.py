# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/12 15:20
# @File    : util.py

import os


def change_html(source_file_path: str, target_file_path: str):
    """
    目前因为输出的html中，会彩色日志的形式，导致log中存在shell在控制台显示的代码
    此方法用于去除生成多余的代码，并生成新的文件，同时删除旧文件

    :param source_file_path:
    :param target_file_path:
    :return:
    """
    with open(source_file_path, encoding='utf-8', mode='r') as rf:
        with open(target_file_path, mode='a+') as wf:

            for i in rf.readlines():
                if '[' in i:
                    i = i.strip()\
                        .replace('[32m', '')\
                        .replace('[0m', '')\
                        .replace('[33m', '')\
                        .replace('[31m', '')\
                        .replace('[91m', '')
                    wf.write(i)
                    wf.write('<br>')
                else:
                    wf.write(i)
    # 删除文件
    os.remove(source_file_path)
