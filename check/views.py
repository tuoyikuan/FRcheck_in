import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.utils import  timezone
from utils.funcs import *
from django.contrib import messages
from pickle import load
import numpy as np
from face_recognition import face_locations, face_encodings, face_distance, load_image_file


@login_required
def check(request, class_id):
    """
    根据班级id返回整个学年签到情况（支持老师和学生两种逻辑）
    """
    length = 0
    class_name = Class.objects.get(id=class_id).class_name
    is_teacher = is_teacher_of(request.user.id, class_id)
    if is_teacher:
        checks = Check.objects.filter(class_id__id=class_id)
        tmplist = []
        for check in checks:
            batch_number = check.batch_number
            date = check.create_time
            sum = 0
            present = 0
            for bit in check.check_string[1:]:
                if bit == '0':
                    sum += 1
                elif bit == '1':
                    sum += 1
                    present += 1
            tmplist.append({
                'number': batch_number,
                'date': date,
                'present': present,
                'sum': sum
            })
            length = len(tmplist)
    else:
        checks = Check.objects.filter(class_id__id=class_id)
        tmplist = []
        for check in checks:
            batch_number = check.batch_number
            date = check.create_time
            s = Student.objects.get(id=request.user)
            class_number = StudentMembership.objects.get(class_id__id=class_id, student=s).class_number
            present = check.check_string[class_number]
            tmplist.append({
                'number': batch_number,
                'date': date,
                'isPresent': present,
            })
            length = len(tmplist)
    return render(request, "check/check.html", {
        "check_lists": tmplist,
        "class_id": class_id,
        "class_name": class_name,
        "isteacher": is_teacher,
        "len": length
    })

@login_required
def teacher_check(request, class_id, check_id):
    # 根据class_id和check_id返回对应某次具体签到活动中每位同学的签到情况
    cl = Class.objects.get(id=class_id)
    students = cl.students.order_by('studentmembership__class_rank').all()
    check_string = Check.objects.get(class_id=cl, batch_number=check_id).check_string
    tmplist = []
    for student in students:
        name = student.id.first_name
        student_id = student.student_id
        present = check_string[StudentMembership.objects.get(student=student, class_id=cl).class_rank]
        tmplist.append({
            'name': name,
            'student_id': student_id,
            'present': present
        })
    return render(request, "check/checkDetail.html", {
        "class_id": class_id,
        "number": check_id,
        "check_id": check_id,
    })

@login_required
def update_check(request, class_id, check_id):
    """需要根据已有的表单信息以及新的图片，把位串与一下"""
    # 读取上传的照片 临时存储在static/file/tmp目录下
    file = request.FILES.get("picture")
    if not file:
        return HttpResponse('no file for upload!')
    path = os.path.join("static/file/tmp", file.name)
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(path, 'wb')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    # 调用模型识别提取照片中的全部人脸特征码
    image = load_image_file(path)
    face_positions = face_locations(image, 2)
    encodings = face_encodings(image, face_positions)

    new_check_string = '0' # 调用人脸识别
    cl = Class.objects.get(id=class_id)
    students = cl.students.order_by('studentmembership__class_rank').all()
    ref_encodings = np.zeros((len(students), 128))
    for i, student in enumerate(students):
        ref_encoding = np.load(os.path.splitext(student.ref_photo_url)[0] + '.npy', allow_pickle=True)
        ref_encodings[i] = ref_encoding
    recognized = np.zeros((len(encodings), len(students)))
    for i, encoding in enumerate(encodings):
        recognized[i] = face_distance(ref_encodings, encoding) <= 0.3
    recognized = recognized.any(axis=0)
    for r in recognized:
        if r:
            new_check_string += '1'
        else:
            new_check_string += '0'
    check = Check.objects.get(class_id=cl, batch_number=check_id)
    check.check_string = new_check_string
    check.save()
    return redirect("/teacherClass/%d/check/teacher/%d" % (class_id, check_id))

@login_required
def create_new(request, class_id):
    check = Check.objects.order_by('-batch_number').first()
    if check:
        check_id_new = check.batch_number + 1
    else:
        check_id_new = 1

    file = request.FILES.get("picture")
    if not file:
        return HttpResponse('no file for upload!')
    path = os.path.join("static/file/tmp", file.name)
    destination = open(path, 'wb')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    # 调用模型识别提取照片中的全部人脸特征码
    image = load_image_file(path)
    face_positions = face_locations(image, 2)
    encodings = np.array(face_encodings(image, face_positions))

    new_check_string = '0'  # 调用人脸识别
    cl = Class.objects.get(id=class_id)
    students = cl.students.order_by('studentmembership__class_rank').all()
    ref_encodings = np.zeros((len(students), 128))
    for i, student in enumerate(students):
        ref_encoding = np.load(os.path.splitext(student.ref_photo_url)[0] + '.npy', allow_pickle=True)
        ref_encodings[i] = ref_encoding
    recognized = np.zeros((len(encodings), len(students)))
    for i, encoding in enumerate(encodings):
        recognized[i] = face_distance(ref_encodings, encoding) <= 0.3
    recognized = recognized.any(axis=0)
    for r in recognized:
        if r:
            new_check_string += '1'
        else:
            new_check_string += '0'
    check = Check(class_id=cl, batch_number=check_id_new, check_string=new_check_string)
    check.save()
    os.remove(path)
    return redirect("/teacherClass/%d/check/teacher/%d" % (class_id, check_id_new))



@login_required
def create(request, class_id):
    class_name = Class.objects.get(id=class_id).class_name

    return render(request, "check/newCheck.html", {
        "class_id": class_id,
        "class_name":  class_name
    })
