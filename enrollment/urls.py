from django.contrib.auth.decorators import login_required
from django.urls import path
from course.views import get_total_amount

from . import views

urlpatterns = [
    path('', login_required(views.index), name='enroll.index'),
    path('create/', login_required(views.create), name="enroll.create"),
    path('get_course_total_amount/', login_required(views.get_course_total_amount),
         name="enroll.get_course_total_amount"),
    path('store/', login_required(views.store), name="enroll.store"),
    path('edit/<int:eid>', login_required(views.edit), name="enroll.edit"),
    path('update/<int:eid>', login_required(views.update), name="enroll.update"),
    path('delete/<int:eid>', login_required(views.delete), name="enroll.delete"),

    # Other URL patterns
    path('course/get_total_amount/', get_total_amount, name='get_total_amount'),
    path('create_enroll/', login_required(views.create), name='course.create'),
    path('update_enroll/<int:cid>/', login_required(views.update), name="course.update"),
]
