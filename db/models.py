from django.db import models
import django.contrib.auth.models as djmod


class User(djmod.User):
    info = models.TextField()


class File(models.Model):
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)


class Student(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    ref_photo_url = models.CharField(max_length=200)


class TA(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    ta_id = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    authority = models.CharField(max_length=100)


class Admin(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)


class Class(models.Model):
    class_name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    info = models.TextField()
    teachers = models.ManyToManyField(
        Teacher,
        through='TeachMembership',
        through_fields=('class_id', 'teacher')
    )
    tas = models.ManyToManyField(
        TA,
        through='TAMembership',
        through_fields=('class_id', 'ta')
    )
    students = models.ManyToManyField(
        Student,
        through='StudentMembership',
        through_fields=('class_id', 'student'),
    )


class Section(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    info = models.TextField(max_length=50)
    files = models.ManyToManyField(
        File,
        through='SectionHasFile',
        through_fields=('section', 'file')
    )


class Check(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    batch_number = models.IntegerField()
    create_time = models.DateField(auto_now=True)
    check_string = models.CharField(max_length=250)


class SectionHasFile(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)


class Problem(models.Model):
    question = models.TextField()
    TYPES = (
        ('CH', 'Choice'),
        ('BK', 'Blank'),
        ('TX', 'Text'),
        ('FL', 'File'),
    )
    type = models.CharField(max_length=2, choices=TYPES)
    key = models.CharField(max_length=50)


class Activity(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    TYPES = [
        ('HW', 'Homework'),
        ('QZ', 'Quiz'),
        ('NT', 'Notification'),
    ]
    type = models.CharField(max_length=2, choices=TYPES)
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    problems = models.ManyToManyField(
        Problem,
        through='ActivityHasProblem',
        through_fields=('activity', 'problem')
    )
    create_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    files = models.ManyToManyField(
        File,
        through='ActivityHasFile',
        through_fields=('activity', 'file')
    )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(due_date__gt=models.F('create_date')), name='check_due_time'),
        ]


class ActivityHasProblem(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)


class Submit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    key = models.TextField()
    file = models.ForeignKey(File, on_delete=models.CASCADE)


class SubmitScore(models.Model):
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now=True)


class ActivityHasFile(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)


class Discuss(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class Post(models.Model):
    discuss = models.ForeignKey(Discuss, on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class Group(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    leader = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leader')
    name = models.CharField(max_length=100)
    ver_number = models.CharField(max_length=100)
    locked = models.BooleanField()
    members = models.ManyToManyField(
        Student,
        through='GroupMembership',
        through_fields=('group', 'student'),
    )


class GroupMembership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class TeachMembership(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class TAMembership(models.Model):
    ta = models.ForeignKey(TA, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class StudentMembership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    class_rank = models.IntegerField()
