from django.http import HttpResponse
from django.shortcuts import render, redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.utils import  timezone
from utils.funcs import *
from django.contrib import messages
import os


@login_required
def check(request, class_id):
    """
    根据班级id返回整个学年签到情况（支持老师和学生两种逻辑）
    """
    is_teacher = is_teacher_of(request.user.id, class_id)
    if is_teacher:
        check_lists = Check.objects.filter(class_id__id=class_id)
        tmplist = []
        for check_list in check_lists:
            number = check_list.number
            date = check_list.create_time
            sum = 0
            present = 0
            for number in check_list.check_string[1:]:
                if number == '0':
                    sum += 1
                elif number == '1':
                    sum += 1
                    present += 1
            tmplist.append({
                'number': number,
                'date': date,
                'present': present,
                'sum': sum
            })
    else:
        check_lists = Check.objects.filter(class_id__id=class_id)
        tmplist = []
        for check_list in check_lists:
            number = check_list.number
            date = check_list.create_time
            present = 0
            s = Student.objects.get(id=request.user)
            class_number = StudentMembership.objects.get(class_id__id=class_id, student=s).class_number
            present = check_list.check_string[class_number]
            tmplist.append({
                'number': number,
                'date': date,
                'present': present,
            })
    return

@login_required
def teacher_check(request, class_id, check_id):
    # 根据class_id和check_id返回对应某次具体签到活动中每位同学的签到情况
    cl = Class.objects.get(id=class_id)
    students = cl.students
    check_string = Check.objects.get(class_id=cl, batch_number=check_id)
    tmplist = []
    for student in students:
        name = student.id.first_name
        student_id = student.student_id
        present = check_string[StudentMembership.objects.get(student=student, class_id=cl).class_number]
        tmplist.append({
            'name': name,
            'student_id': student_id,
            'present': present
        })
    return

@login_required
def update_check(request, class_id, check_id):
    """需要根据已有的表单信息以及新的图片，把位串与一下"""
    new_check_string = '0' # 调用人脸识别
    cl = Class.objects.get(id=class_id)
    students = cl.students.all().order_by('studentmembership__class_number')
    for student in students:
        pass
    check_string = Check.objects.get(class_id=cl, batch_number=check_id)
    return redirect("/teacherClass/%d/check/teacher/%d" % (class_id, check_id))

@login_required
def create(request, class_id):
    checks = Check.objects.filter().all()
    check_id_new = checks[-1].batch_number + 1
    cl = Class.objects.get(id=class_id)
    check = Check(class_id=cl, batch_number=check_id_new, check_string="0")
    check.save()

    # 将签到结果返回给Client
    return redirect("/teacherClass/%d/check" %class_id)