from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db import models

def main(request):
#    recent_info_lists = models.notification.filter(studentId = sid, id > )
#  myclass_lists = models.myclass.filter(studentId = sid, id > )

    return render(request, 'student/studentMain.html')
#,{'recent_notfication_lists':recent_info_lists, ''})
