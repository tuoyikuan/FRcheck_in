# noting to do here, only redirect in urls.py
from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from utils.funcs import *

# Create your views here.
import pdb

signal = 0
signal1 = 0


@login_required
def allClass(request):
    usr = request.user.username
    class_list_t = []
    class_list_s = []
    try:
        t = Teacher.objects.get(id__username=usr)
        class_list_t = TeachMembership.objects.filter(teacher=t)
    except: pass
    try:
        s = Student.objects.get(id__username=usr)
        class_list_s = StudentMembership.objects.filter(student=s)
    except: pass
    length = len(class_list_s)+len(class_list_t)
    tmplist = []
    for cl in class_list_s:
        tmplist.append({
            'class_id': cl.class_id.id,
            'class_name': cl.class_id.class_name + '（课程代码：' + str(cl.class_id.id) + '）',
            'class_info': (cl.class_id.info if len(cl.class_id.info) else "暂无简介")[:100],
            'color': '#ffffff',
        })
    for cl in class_list_t:
        tmplist.append({
            'class_id': cl.class_id.id,
            'class_name': cl.class_id.class_name+' （教师界面, 课程代码：' + str(cl.class_id.id) + '）',
            'class_info': (cl.class_id.info if len(cl.class_id.info) else "暂无简介")[:100],
            'color': '#e0ffff',
        })
    global signal, signal1
    temp = signal
    signal = 0
    temp1 = signal1
    signal1 = 0
    return render(request, "teacher/teacherClass.html", {
        'class_list': tmplist,
        'username': usr,
        'len': length,
        'signal': temp,
        'signal1': temp1,
        'isteacher': is_teacher(request.user.id),
    })


@login_required
def addClass(request):
    global signal
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        usr = request.user.username
        t = Student.objects.get(id__username=usr)
        try:
            cl = Class.objects.filter(id=class_id)
        except Exception as e:
            signal = 1
            return redirect("/teacherClass/allClass")
        if len(cl) != 0:
            cl[0].students.add(t)
            cl[0].save()
            signal = 2
        else:
            signal = 1
    return redirect("/teacherClass/allClass")


@login_required
def createClass(request):
    global signal1
    if request.method == 'POST':
        # return redirect("/teacherClass/allClass")
        class_name = request.POST.get('class_name')
        class_info = request.POST.get('class_info')
        usr = request.user.username
        t = Teacher.objects.get(id__username=usr)

        try:
            cl = Class.objects.filter(class_name=class_name)
        except Exception as e:
            signal1 = 1
            return redirect("/teacherClass/allClass")
        if len(cl) == 0:
            newClass = Class(class_name=class_name, info=class_info)
            newClass.teachers.add(t)
            newClass.save()
            signal1 = 2
        else:
            signal1 = 1
    return redirect("/teacherClass/allClass")
