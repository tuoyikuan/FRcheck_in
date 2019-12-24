from django.shortcuts import render

# Create your views here.


def show_group(request, class_id):
    return render(request, 'group/group.html', {
        'class_id': class_id,
    })