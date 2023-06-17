from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import *
urlpatterns = [

    path('student-courses/', views.student_courses, name='student-courses'),
    path('private-courses/<str:role>/', views.private_courses, name='private-courses'),
    path('student-path/', views.student_path, name='student-path'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('student-quiz-result-details/<int:id>/', views.student_quiz_result_details, name='student-quiz-result-details'),
    path('student-quiz-results/', views.student_quiz_results, name='student-quiz-results'),
    path('student-take-course/', views.student_take_course, name='student-take-course'),
    path('student-take-lesson/', views.student_take_lesson, name='student-take-lesson'),
    path('student-take-quiz/', views.student_take_quiz, name='student-take-quiz'),
    path('student-quiz-results/', views.student_quiz_results, name='student-quiz-results'),
    path('quizzes/<str:role>/', views.quizzes, name='quizzes'),
    path('student-course/<int:id>/', views.teacher_course, name='teacher-course'),

        path('teacher-showquiz/<int:id>/', views.teacher_showquiz, name='teacher-showquiz'),

    path('teacher-mycourses/', views.teacher_mycourses, name='teacher-mycourses/'),
    path('teacher-addcourse/', views.teacher_addcourse, name='teacher-addcourse'),
    path('teacher-addchapter/<int:id>/', views.teacher_addchapter, name='teacher-addchapter'),
    path('teacher-course/<int:id>/', views.teacher_course, name='teacher-course'),
    path('teacher-coursefeedback/<int:id>/', views.teacher_coursefeedback, name='teacher-coursefeedback'),
    path('teacher-addcourses/', views.teacher_addcourses, name='teacher-addcourses'),
    path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    path('teacher-quizzes/', views.quizzes, name='teacher-quizzes'),
    path('teacher-addquizz/', views.teacher_addquizz, name='teacher-addquizz'),
    path('instructor-edit-quiz/', views.instructor_edit_quiz, name='instructor-edit-quiz'),

    path('index', views.index, name='index'),
    path('showquiz/<int:id>/<str:role>/', views.showquiz, name='showquiz'),
    path('login/', views.login, name='login'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('chapter/<int:id>/', views.chapter, name='chapter'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-account-profile', views.edit_account_profile, name='edit-account-profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)