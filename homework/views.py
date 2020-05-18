from django.shortcuts import render
from utils.funcs import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.

@login_required
def homework(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    temp = Activity.objects.filter(class_id=class_id, type='Homework')
    templist = []
    for e in temp:
        templist.append({
            'act_id': e.id,
            'title': e.title,
            'content': e.content,
            'create_date': e.create_date,
            'author': e.author.username,
            'class_id': class_id,
            'due_date': e.due_date,
        })
    return render(request, 'homework/homework.html', {
        'act_list': templist,
        'class_id': class_id,
        'isteacher': is_teacher_of(request.user.id, class_id),
    })


@login_required
def create_act(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, "homework/new_act.html", {"class_id" : class_id})


@login_required
def show_act_detail(request, class_id, act_id):
    temp = Activity.objects.get(id=act_id)
    #if not in_class(request.user.id, temp.class_id_id):
        #return redirect('/teacherClass/denied')
    homework_list = temp.problems.all()
    homeworks = []
    for h in homework_list:
        if h.type == "Choice":
            type = "选择题"
            index_a = h.question.index("<A>")
            question = h.question[0: int(index_a)]
            if len(question) > 10:
                question = question[0:9]+"..."
            homeworks.append({
                "problem_id": h.id,
                "type": type,
                "question": question,
                "author": temp.author,
            })
        elif h.type == "Blank":
            type = "填空题"
            index_num = h.question.index("<number>")
            question = h.question[0:index_num]
            if len(question) > 10:
                question = question[0:9]+"..."
            homeworks.append({
                "problem_id": h.id,
                "type": type,
                "question": question,
                "author": temp.author,
            })
        else:
            question = h.question
            type = "简答题"
            if len(question) > 10:
                question = question[0:9]+"..."
            homeworks.append({
                "problem_id": h.id,
                "type": type,
                "question": question,
                "author": temp.author,
            })
    return render(request, "homework/show_act.html", {
        "homework_list" : homeworks,
        "class_id" : class_id,
        "isteacher" : is_teacher_of(request.user.id, class_id),
        "act_id" : act_id,
    })


@login_required
def new_act(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    #if not is_teacher_of(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        title = request.POST.get('act-title')
        due_date = request.POST.get('due_date')
        due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
        activity = Activity(
            class_id_id=class_id,
            type='Homework',
            title=title,
            # content=content,
            author_id=request.user.id,
            due_date=due_date,
        )
        activity.save()
    return redirect("/teacherClass/%d/homework" % class_id)


@login_required
def delete_act(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    #if not is_teacher_of(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    activite = Activity.objects.get(id=act_id)
    activite.delete()
    return redirect("/teacherClass/%d/homework" % class_id)


@login_required
def create_blank(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, "homework/new_blank.html", {"class_id": class_id, "act_id": act_id})


@login_required
def create_choose(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, "homework/new_choose.html", {"class_id": class_id, "act_id": act_id})


@login_required
def create_text(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, "homework/new_text.html", {"class_id": class_id, "act_id": act_id})


@login_required
def create_ch(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    #if not is_teacher_of(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        question = request.POST.get("question")
        choose_a = request.POST.get("choose_a")
        choose_b = request.POST.get("choose_b")
        choose_c = request.POST.get("choose_c")
        choose_d = request.POST.get("choose_d")
        question = question + "<A>" + choose_a + "<B>" + choose_b + "<C>" + choose_c + "<D>" + choose_d
        key_list = request.POST.getlist("answer_list")
        key=""
        for answer in key_list:
            key += answer
        activity = Activity.objects.get(id=act_id)
        problem = Problem(
            question=question,
            type="Choice",
            key=key,
        )
        problem.save()
        activity.problems.add(problem)
        return redirect("/teacherClass/%d/homework/check/%d" % (class_id, act_id))


@login_required
def create_bk(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    #if not is_teacher_of(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        question = request.POST.get("question")
        number = request.POST.get("number")
        key = request.POST.get("answer")
        question = question+"<number>"+number
        activity = Activity.objects.get(id=act_id)
        problem = Problem(
            question=question,
            type="Blank",
            key=key,
        )
        problem.save()
        activity.problems.add(problem)
        return redirect("/teacherClass/%d/homework/check/%d" % (class_id, act_id))


@login_required
def create_tx(request, class_id, act_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    #if not is_teacher_of(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        question = request.POST.get("question")
        key = request.POST.get("answer")
        activity = Activity.objects.get(id=act_id)
        problem = Problem(
            question=question,
            type="Text",
            key=key,
        )
        problem.save()
        activity.problems.add(problem)
        return redirect("/teacherClass/%d/homework/check/%d" % (class_id, act_id))


'''
@login_required
def create_fl(request, class_id, homework_id):
    if not in_class(request.user.id, class_id):
        return redirect('/teacherClass/denied')
    if not is_teacher_of(request.user.id, class_id):
        return redirect('/teacherClass/denied')
    if request.method == 'POST':
        title = request.POST.get('homework-title')
'''


@login_required
def show_problem(request, class_id, act_id, problem_id):
    h = Problem.objects.get(id=problem_id)
    temp = Activity.objects.get(id=act_id)
    if h.type == "Choice":
        type = "选择题"
        index_a = h.question.index("<A>")
        index_b = h.question.index("<B>")
        index_c = h.question.index("<C>")
        index_d = h.question.index("<D>")
        question = h.question[0: int(index_a)]
        choose_a = h.question[int(index_a + 3): int(index_b)]
        choose_b = h.question[int(index_b + 3): int(index_c)]
        choose_c = h.question[int(index_c + 3): int(index_d)]
        choose_d = h.question[int(index_d + 3): len(h.question)]
        if len(question) > 10:
            question = question[0:9] + "..."
        return render(request, "homework/show_choose.html", {
            "problem_id": h.id,
            "type": type,
            "question": question,
            "choose_a": choose_a,
            "choose_b": choose_b,
            "choose_c": choose_c,
            "choose_d": choose_d,
            "author": temp.author,
            "class_id": class_id,
            "act_id": act_id,
            "isteacher" : is_teacher_of(request.user.id, class_id),
        })
    elif h.type == "Blank":
        type = "填空题"
        index_num = h.question.index("<number>")
        question = h.question[0:index_num]
        number = int(h.question[-1:])
        if len(question) > 10:
            question = question[0:9] + "..."
        return render(request, "homework/show_blank.html", {
            "problem_id": h.id,
            "type": type,
            "question": question,
            "number": number,
            "author": temp.author,
            "class_id": class_id,
            "act_id": act_id,
            "isteacher": is_teacher_of(request.user.id, class_id),
        })
    else:
        question = h.question
        type = "简答题"
        if len(question) > 10:
            question = question[0:9] + "..."
        return render(request, "homework/show_text.html", {
            "problem_id": h.id,
            "type": type,
            "question": question,
            "author": temp.author,
            "class_id": class_id,
            "act_id": act_id,
            "isteacher": is_teacher_of(request.user.id, class_id),
        })


@login_required
def submit_problem(request, class_id, act_id, problem_id):
    problem = Problem.objects.get(id=problem_id)
    user = request.user.id
    student = Student.objects.get(id=user)
    sub = Submit.objects.filter(student_id=student.id_id, problem_id=problem.id)
    if problem.type == "Choice":
        key_list = request.POST.getlist("answer_list")
        key = ""
        for answer in key_list:
            key += answer
    elif problem.type == "Blank":
        key = request.POST.get("answer")
    else:
        key = request.POST.get("answer")
    if len(sub) == 0:
        submit = Submit(key=key, problem=problem, student_id=student.id_id, file_id=1)
        submit.save()
    else:
        sub[0].key = key
        sub[0].save()
    return redirect("/teacherClass/%d/homework/check/%d" % (class_id, act_id))


@login_required
def student_submit(request, class_id, act_id, problem_id):
    submits = Submit.objects.filter(problem_id=problem_id).all()
    problem = Problem.objects.get(id=problem_id)
    all = []
    for submit in submits:
        subscore = SubmitScore.objects.filter(submit_id=submit.id).all()
        user = User.objects.get(id=submit.student_id)
        if len(subscore)>0:
            all.append({
                "submit_id": submit.id,
                "student": user.username,
                "key": submit.key,
                "score": subscore[0].score,
            })
        else:
            all.append({
                "submit_id": submit.id,
                "student": user.username,
                "key": submit.key,
                "score": "未评分",
            })
    return render(request, "homework/show_submit.html", {
        "submit_list": all,
        "type": problem.type,
        "class_id": class_id,
        "act_id": act_id,
        "problem_id": problem_id,
    })


@login_required
def score(request, class_id, act_id, problem_id, submit_id):
    submit = Submit.objects.get(id=submit_id)
    problem = Problem.objects.get(id=submit.problem_id)
    if problem.type == "Choice":
        index_a = problem.question.index("<A>")
        question = problem.question[0: int(index_a)]
    elif problem.type == "Blank":
        index_num = problem.question.index("<number>")
        question = problem.question[0:index_num]
    else:
        question = problem.question
    return render(request, "homework/score.html", {
        "class_id": class_id,
        "act_id": act_id,
        "problem_id": problem_id,
        "submit_id": submit_id,
        "question": question,
        "answer": problem.key,
        "submit": submit.key,
    })

@login_required
def upscore(request, class_id, act_id, problem_id, submit_id):
    username = request.user.username
    usr = User.objects.get(username=username)
    if request.method == "POST":
        submit = Submit.objects.get(id=submit_id)
        submit_score = SubmitScore.objects.filter(submit_id=submit_id).all()
        score = request.POST.get("score")
        if len(submit_score) > 0:
            sub_score = SubmitScore.objects.get(submit_id=submit_id)
            sub_score.score = score
            sub_score.save()
        else:
            subscore = SubmitScore(
                submit=submit,
                rater=usr,
                score=score,
            )
            subscore.save()
    return redirect("/teacherClass/%d/homework/%d/problem/%d/student_submit" % (class_id, act_id, problem_id))
