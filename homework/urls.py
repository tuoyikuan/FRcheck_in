from django.urls import path, include
from homework.views import *

urlpatterns = [
    path("", homework),
    path(r"check/<int:act_id>/", show_act_detail),
    path(r"create/", create_act),
    path(r"new_act/", new_act),
    path(r"<int:act_id>/delete/", delete_act),
    path(r"<int:act_id>/create/", create_text),
    path(r"<int:act_id>/create/text/", create_text),
    path(r"<int:act_id>/create/choose/", create_choose),
    path(r"<int:act_id>/create/blank/", create_blank),
    path(r"<int:act_id>/create/text/submit/", create_tx),
    path(r"<int:act_id>/create/choose/submit/", create_ch),
    path(r"<int:act_id>/create/blank/submit/", create_bk),
    path(r"<int:act_id>/problem/<int:problem_id>/", show_problem),
    path(r"<int:act_id>/problem/<int:problem_id>/submit/", submit_problem),
    path(r"<int:act_id>/problem/<int:problem_id>/student_submit/", student_submit),
    path(r"<int:act_id>/problem/<int:problem_id>/score/<int:submit_id>/", score),
    path(r"<int:act_id>/problem/<int:problem_id>/up_score/<int:submit_id>/", upscore),
]