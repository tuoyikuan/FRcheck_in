from django.shortcuts import render, redirect
from db.models import *

# Create your views here.
def section(request):
    class_id = request.GET.get('class_id')

    """section"""
    sections = Section.objects.filter(class_id__id=class_id).all()
    tmpSection = []
    for section in sections:
        tmpSection.append({
            'section_name': section.name
        })

    return render(request, "student/studentClassSection.html", {"class_id": class_id})