from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('student-path/', views.student_path, name='student-path'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('student-student-quiz-result-details/', views.student_quiz_result_details, name='student-student-quiz-result-details'),
    path('student-quiz-results/', views.student_quiz_results, name='student-quiz-results'),
    path('student-take-course/', views.student_take_course, name='student-take-course'),
    path('student-take-lesson/', views.student_take_lesson, name='student-take-lesson'),
    path('student-take-quiz/', views.student_take_quiz, name='student-take-quiz'),
    path('student-quiz-results/', views.student_quiz_results, name='student-quiz-results'),
    #path('teacher_mycourses/', views.teacher_mycourses, name='teacher_mycourses/'),
    #path('teacher_addcourse/', views.teacher_addcourse, name='teacher_addcourse'),

    path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    path('aboutus/', views.aboutus, name='aboutus'),
   # path('enter_login/', views.enter_login, name='enter_login'),
    path('signup/', views.signup, name='signup'),
    #path('signingup/', views.signingup, name='signingup'),
    path('logout/',views.logout,name='logout'),
    path('profile/', views.profile, name='profile'),
]