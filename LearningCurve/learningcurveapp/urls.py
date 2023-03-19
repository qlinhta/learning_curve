from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('student-path/', views.student_path, name='student-path'),
    path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    path('aboutus/', views.aboutus, name='aboutus'),
]