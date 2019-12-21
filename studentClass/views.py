from django.shortcuts import render
from studentClass import models
# Create your views here.
def allClass(request):
    return render(request, "student/studentClass.html")



def addClass(request):
    if request.method == 'POST':
        classId = request.POST.get("classId")
    return render(request, "student/studentClass.html")
