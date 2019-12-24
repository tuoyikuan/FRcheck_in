from django.shortcuts import render, redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from utils.funcs import *

@login_required
def section(request, class_id):
    """section"""
    class_name = Class.objects.get(id=class_id).class_name
    sections = Section.objects.filter(class_id__id=class_id).all()
    length = len(sections)
    tmpSection = []
    numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
    for section in sections:
        tmpSection.append({
            'section_name': section.name,
            'number': section.number,
            'section_number': numbers[section.number]
        })
    return render(request, "student/studentClassSection.html", {"class_id": class_id, "section_lists": tmpSection, "class_name": class_name, "len": length})


@login_required
def show_sec(request, class_id, sec_number):
    class_name = Class.objects.get(id=class_id).class_name
    section = Section.objects.get(class_id__id=class_id, number=sec_number)
    numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
    section_detail = {
        "section_name": section.name,
        "number": section.number,
        "section_number": numbers[section.number],
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
        return render(request, "student/show_sec.html", {"class_id": class_id, "section": section_detail, "flen": flen, "class_name": class_name, "file_lists": tmp_file_lists})
    else:
        return render(request, "student/show_sec.html", {"class_id": class_id, "section": section_detail, "flen": flen, "class_name": class_name})


@login_required
def create_new_sec(request, class_id):
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        info = request.POST.get("info")
        cl = Class.objects.get(id=class_id)
        if len(Section.objects.filter(class_id=cl, number=number).all()) == 0:
            sec = Section(class_id=cl, name=name, number=number, info=info)
            sec.save()
            return redirect("/studentCLass/%d/section" %(class_id))
        else:
            return redirect("/studentCLass/%d/section" %(class_id))


@login_required
def create(request, class_id):
    return render(request, "student/newSection.html", {"class_id": class_id})