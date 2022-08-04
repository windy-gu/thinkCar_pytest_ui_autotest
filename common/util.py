# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/7/12 15:20
# @File    : util.py

import os


def change_html(source_file_path: str, target_file_path: str = None):
    """
    将html报告中日志输出颜色跟控制保持一致

    :param source_file_path:
    :param target_file_path:
    :return:
    """
    with open(source_file_path, encoding='utf-8', mode='r') as rf:
        with open(target_file_path, mode='a+') as wf:

            for i in rf.readlines():
                # 次数if 是为了避免前端html报告中存在error异常
                if '<br/></div></td></tr></tbody></table></body></html>' in i:
                    i_front, i_latest = i.split('<br/></div></td></tr></tbody></table></body></html>')
                    i = i_front
                    i_latest = '<br/></div></td></tr></tbody></table></body></html>'
                # 绿色展示日志内容
                if ' - INFO - ' in i:
                    i = i.replace('\n', '')
                    i_front, i_back = i.split(' - INFO - ')
                    wf.write(i_front + ' - INFO - ' + '<span class="passed">' + i_back + '</span>' + '\n')
                # 黄色展示日志内容
                elif ' - WARNING - ' in i:
                    i = i.replace('\n', '')
                    i_front, i_back = i.split(' - WARNING - ')
                    wf.write(i_front + ' - WARNING - ' + '<span class="skipped">' + i_back + '</span>' + '\n')
                # 红色展示日志内容
                elif ' - ERROR - ' in i:
                    i = i.replace('\n', '')
                    i_front, i_back = i.split(' - ERROR - ')
                    wf.write(i_front + ' - ERROR - ' + '<span class="error">' + i_back + '</span>' + '\n')
                # 红色展示日志内容
                elif ' - CRITICAL - ' in i:
                    i = i.replace('\n', '')
                    i_front, i_back = i.split(' - CRITICAL - ')
                    wf.write(i_front + ' - CRITICAL - ' + '<span class="error">' + i_back + '</span>' + '\n')
                else:
                    wf.write(i)
            wf.write(i_latest)
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
