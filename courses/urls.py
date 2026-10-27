from django.urls import path
from . import views

urlpatterns = [
    path('', views.offering_list, name='offering_list'),
    path('enroll/<int:offering_id>/', views.enroll, name='enroll'),
    path('drop/<int:offering_id>/', views.drop, name='drop'),
    path('timetable/', views.my_timetable, name='my_timetable'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/offering/<int:offering_id>/students/', views.teacher_offering_students, name='teacher_offering_students'),
]

