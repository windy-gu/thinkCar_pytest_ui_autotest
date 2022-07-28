# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/12 15:20
# @File    : util.py

import os


def change_html(source_file_path: str, target_file_path: str = None):
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
                if ' - INFO - ' in i:
                    i_front, i_back = i.split(' - INFO - ')
                    wf.write(i_front + ' - INFO - ')
                    wf.write('<span class="passed">')
                    wf.write(i_back)
                    wf.write('</span>')
                elif ' - WARNING - ' in i:
                    i_front, i_back = i.split(' - WARNING - ')
                    wf.write(i_front + ' - WARNING - ')
                    wf.write('<span class="skipped">')
                    wf.write(i_back)
                    wf.write('</span>')
                elif ' - ERROR - ' in i:
                    i_front, i_back = i.split(' - ERROR - ')
                    wf.write(i_front + ' - ERROR - ')
                    wf.write('<span class="error">')
                    wf.write(i_back)
                    wf.write('</span>')
                elif ' - CRITICAL - ' in i:
                    i_front, i_back = i.split(' - CRITICAL - ')
                    wf.write(i_front + ' - CRITICAL - ')
                    wf.write('<span class="error">')
                    wf.write(i_back)
                    wf.write('</span>')
                else:
                    wf.write(i)
    # 删除文件
    os.remove(source_file_path)


def str_transform_dict(temp_str: str) -> dict:
    """
    将符合key=value类型的str内容，转换为{key:value} 输出
    :param temp_str:
    :return:
    """
    temp_dict = {}
    temp_str_temp = temp_str.replace('"', '')
    temp_split_list = temp_str_temp.split(',')
    for i in range(len(temp_split_list)):
        temp_str_1 = temp_split_list[i].replace(' ', '')
        k, v = temp_str_1.split('=')
        if len(v) == 1:
            if 48 <= ord(v) <= 57:
                v = int(v)
        temp_dict[k] = v
    return temp_dict
