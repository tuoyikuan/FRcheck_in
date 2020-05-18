from db.models import *
from os.path import splitext
from pickle import dump
from face_recognition import face_encodings, load_image_file


def in_class(user_id, class_id):
    try:
        cl = Class.objects.get(id=class_id)
        return (Student.objects.get(id__id=user_id) in cl.students.all() or
                Teacher.objects.get(id__id=user_id) in cl.teachers.all() or
                TA.objects.get(id__id=user_id) in cl.tas.all())
    except Exception as e:
        return False


def is_student_of(user_id, class_id):
    try:
        cl = Class.objects.get(id=class_id)
        return Student.objects.get(id__id=user_id) in cl.students.all()
    except Exception as e:
        return False


def is_teacher_of(user_id, class_id):
    try:
        cl = Class.objects.get(id=class_id)
        return Teacher.objects.get(id__id=user_id) in cl.teachers.all()
    except Exception as e:
        return False


def is_ta_of(user_id, class_id):
    try:
        cl = Class.objects.get(id=class_id)
        return TA.objects.get(id__id=user_id) in cl.tas.all()
    except Exception as e:
        return False


def is_leader_of(user_id, group_id):
    try:
        gr = Group.objects.get(id=group_id)
        return gr.leader.id.id == user_id
    except Exception as e:
        return False

def is_teacher(user_id):
    try:
        Teacher.objects.get(id__id=user_id)
        return True
    except Exception as e:
        return False
    
def get_class_name(class_id):
    try:
        c = Class.objects.get(id=class_id)
        return c.class_name
    except Exception as e:
        return None

def generate_face_encoding(student_id):
    student = Student.objects.get(student_id=student_id)
    path = student.ref_photo_url
    ref_photo = load_image_file(path)
    return dump(face_encodings(ref_photo), splitext(path)[0] + '.pkl')


