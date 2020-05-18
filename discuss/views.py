from django.shortcuts import render
from db.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utils.funcs import *
# Create your views here.


@login_required()
def user_name(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, 'discuss/teacherMain.html')


@login_required()
def message_chat(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    temp = Discuss.objects.filter(class_id=class_id).order_by('-create_time')
    templist=[]
    for e in temp:
        templist.append({
            'name': e.author.username,
            'time_str': e.create_time,
            'content': e.content,
            'title': e.title,
            'id': e.id,
        })
    return render(request, 'discuss/message-chat.html', {
        'post_list': templist,
        'class_id': class_id,
        'current_user': request.user.username,
        'is_teacher': is_teacher_of(request.user.id, class_id),
    })


@login_required()
def create_msg(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        title = request.POST.get('msg_title')
        content = request.POST.get('msg_content')
        Discuss.objects.create(
            class_id=Class.objects.get(id=class_id),
            title=title,
            content=content,
            author=User.objects.get(id=request.user.id),
        )
        return redirect('/teacherClass/%d/discuss/' % class_id)
    return redirect('/teacherClass/%d/discuss/' % class_id)


@login_required()
def delete_msg(request, class_id, e_id):
    temp = Discuss.objects.get(id=e_id)
    class_id1 = temp.class_id.id
    #if not in_class(request.user.id, class_id1):
        #return redirect('/teacherClass/denied')
    userid=request.user.id
    #if temp.author.id != userid and not is_teacher_of(userid, class_id1):
        #return redirect('/teacherClass/denied')
    temp.delete()
    return redirect('/teacherClass/%d/discuss/' % class_id1)


@login_required()
def chatting(request, class_id, e_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    temp = Post.objects.filter(discuss=e_id)
    templist = []
    t = Discuss.objects.get(id=e_id)
    tlist = {
        'name': t.author.username,
        'time_str': t.create_time,
        'content': t.content,
        'title': t.title,
        'id': t.id,
        'class_id': class_id,
    }
    for e in temp:
        templist.append({
            'name': e.author.username,
            'time_str': e.create_time,
            'content': e.content,
            'id': e.id,
        })
    return render(request, 'discuss/chatting.html', {
        'post_list': tlist,
        'current_user': request.user.username,
        'reply_list': templist,
        'is_teacher': is_teacher_of(request.user.id, class_id),
        'class_id': class_id
    })


@login_required()
def discuss_root(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return redirect('/teacherClass/%d/discuss/' % class_id)


def create_post(request, class_id, e_id):
    if request.method == 'POST':
        content = request.POST.get('msg_content')
        Post.objects.create(
            discuss=Discuss.objects.get(id=e_id),
            content=content,
            author=User.objects.get(id=request.user.id),
        )
        return redirect('/teacherClass/%d/discuss/chatting/%d' % (class_id, e_id))
    return redirect('/teacherClass/%d/discuss/chatting/%d' % (class_id, e_id))


def delete_post(request, class_id, e_id, post_id):
    temp = Post.objects.get(id=post_id)
    temp.delete()
    return redirect('/teacherClass/%d/discuss/chatting/%d' % (class_id, e_id))