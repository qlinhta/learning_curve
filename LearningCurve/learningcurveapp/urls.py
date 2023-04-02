from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('student-path/', views.student_path, name='student-path'),
    path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    path('aboutus/', views.aboutus, name='aboutus'),
   # path('enter_login/', views.enter_login, name='enter_login'),
    path('signup/', views.signup, name='signup'),
    #path('signingup/', views.signingup, name='signingup'),
    path('logout/',views.logout,name='logout'),
    path('profile/', views.profile, name='profile'),
]