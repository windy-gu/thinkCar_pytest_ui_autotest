# UI_autotest

## 安装依赖
```shell
pip3 install -r requirements.txt
```

## 导出requirements.txt
```shell
pip3 freeze > requirements.txt
```

## 执行
```python
1）通过主程序run.py运行test_dir目录下满足条件的所有testcase
2）执行指定testcase文件里
if __name__ == '__main__':
    file_name = os.path.split(__file__)[-1]
    pytest.main(['-s', '-v', './{}'.format(file_name)])
```

## 元素定位
```
支持定位类型
"text",
"textContains",
"textMatches",
"textStartsWith",
"className",
"classNameMatches",
"description",
"descriptionContains",
"descriptionMatches",
"descriptionStartsWith",
"checkable",
"checked",
"clickable",
"longClickable",
"scrollable",
"enabled",
"focusable",
"focused",
"selected",
"packageName",
"packageNameMatches",
"resourceId",
"resourceIdMatches",
"index",
"instance"

eg：login_button = Element(resourceId="com.us.thinktool:id/right_button_text", text="登錄", describe='登錄_btn')
# 这里同时取了两个定位类型：resourceId 和 text，describe不是定位类型只是为了方便日志输出的字段

高级用法 child, sibling, right, left, up, down暂时未实现
```