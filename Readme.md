# 注意事项

## 写代码过程中遇到的注意事项请添加至此

### 1. 各界面不写侧边栏

在template下有一个`common.html`，内容如下

```
侧边栏balabala
{% block 'kk' %}
{% endblock %}
侧边栏balabala
```

每个自己的界面写成如下格式：

```
{% extends 'commom.html' %}
{% block 'kk' %}
{% load static %}
你的页面balabala
{% endblock %}
```

### 2. 各文件夹功能

建议使用`pycharm`

项目主目录`demo`

模板目录`template`

静态资源目录`static`

虚拟python环境`venv`

其他为模块目录

### 3. 数据库模块使用方式

example

```python
from db.models import *   """告诉函数有哪些类"""
from django.db import models  """import数据库"""

def func1():
    user=User(name='foo', pwd='foopwd', info='')
    user.save()
    student=Student(id=user.id, student_id='3170108888', dept='CS')
    student.save()
	cl=Class(class_name='fooclass', info='')
    cl.save()
    cl.students.add(student)
    student_lists = models.Student.objects.filter(id>5).all()
```

更多示例查看`notification`模块及官方文档。

注意：不要给`create_date`赋值，所有值不能留空，遇到不需要的值应填入空字符串

