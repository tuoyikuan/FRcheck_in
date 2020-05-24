from django.http import HttpResponse
from django.shortcuts import render, redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from utils.funcs import *
from django.contrib import messages
import os

@login_required
def section(request, class_id):
    """section"""
    class_name = Class.objects.get(id=class_id).class_name
    sections = Section.objects.filter(class_id__id=class_id).all()
    length = len(sections)
    tmpSection = []
    for section in sections:
        tmpSection.append({
            'section_name': section.name,
            'number': section.number,
            'section_number':section.number
        })
    return render(request, "teacher/teacherClassSection.html", {
        "class_id": class_id,
        "section_lists": tmpSection,
        "class_name": class_name,
        "len": length,
        "isteacher": is_teacher_of(request.user.id, class_id),
    })


@login_required
def show_sec(request, class_id, sec_number):
    class_name = Class.objects.get(id=class_id).class_name
    section = Section.objects.get(class_id__id=class_id, number=sec_number)
    section_detail = {
        "section_name": section.name,
        "number": section.number,
        "section_number": section.number,
        "info": section.info,
    }
    file_lists = section.files.all()
    flen = len(file_lists)
    if flen:
        tmp_file_lists = []
        for file in file_lists:
            tmp_file_lists.append({
                "url": file.url,
                "name": file.name
            })
            print(file.url)
        return render(request, "teacher/show_sec.html", {
            "class_id": class_id,
            "section": section_detail,
            "flen": flen,
            "class_name": class_name,
            "file_lists": tmp_file_lists,
            "isteacher": is_teacher_of(request.user.id, class_id),
        })
    else:
        return render(request, "teacher/show_sec.html", {
            "class_id": class_id,
            "section": section_detail,
            "flen": flen,
            "class_name": class_name,
            "isteacher": is_teacher_of(request.user.id, class_id),
        })


@login_required
def create_new_sec(request, class_id):
    global newsection
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        info = request.POST.get("info")
        cl = Class.objects.get(id=class_id)
        if len(Section.objects.filter(class_id=cl, number=number).all()) == 0:
            sec = Section(class_id=cl, name=name, number=number, info=info)
            sec.save()
            messages.success(request, "成功创建新章节")
        else:
            messages.success(request, "创建新章节失败，章节已存在")
    return redirect("/teacherClass/%d/section" %class_id)

@login_required
def create(request, class_id):
    return render(request, "teacher/newSection.html", {"class_id": class_id,"class_name": Class.objects.get(id=class_id).class_name})

@login_required
def uploadFile(request, class_id, sec_number):
    usr = request.user.username
    rusr = User.objects.get(username=usr)
    if request.method == 'POST':
        file = request.FILES.get("file")
        if not file:
            return HttpResponse('no file for upload!')
        path = os.path.join("static/file", str(class_id),str(sec_number))
        if os.path.exists(path) == False:
            os.makedirs(path)
        destination = open(os.path.join(path,file.name) , 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        url = os.path.join("file", str(class_id),str(sec_number), file.name)
        # print(url)
        newFile = File(url=url, name=file.name, uploader=rusr)
        newFile.save()
        Asection = Section.objects.get(class_id=class_id, number=sec_number)
        Asection.files.add(newFile)
    return redirect("/teacherClass/%d/section/detail/%d/" % (class_id, sec_number))
