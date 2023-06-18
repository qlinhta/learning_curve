from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import *
urlpatterns = [



    path('student-path/', views.student_path, name='student-path'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('student-quiz-result-details/<int:id>/', views.student_quiz_result_details, name='student-quiz-result-details'),
    path('student-quiz-results/', views.student_quiz_results, name='student-quiz-results'),
    path('student-feedback/<int:id>/', views.student_feedback, name='student-feedback'),
    path('student-chapter-complete/<int:id>/', views.student_chapter_complete, name='student-chapter-complete'),




    path('teacher-showquiz/<int:id>/', views.teacher_showquiz, name='teacher-showquiz'),
    path('teacher-addcourse/', views.teacher_addcourse, name='teacher-addcourse'),
    path('teacher-addchapter/<int:id>/', views.teacher_addchapter, name='teacher-addchapter'),
    path('teacher-addquizz/', views.teacher_addquizz, name='teacher-addquizz'),

    path('chapter/<str:role>/<int:id>', views.chapter, name='chapter'),
    path('coursefeedback/<int:id>/<str:role>/', views.coursefeedback, name='coursefeedback'),
    path('quizzes/<str:role>/', views.quizzes, name='quizzes'),
    path('showquiz/<int:id>/<str:role>/', views.showquiz, name='showquiz'),

    path('instructor-edit-quiz/', views.instructor_edit_quiz, name='instructor-edit-quiz'),
    path('edit-account-profile', views.edit_account_profile, name='edit-account-profile'),

    path('private-courses/<str:role>/', views.private_courses, name='private-courses'),
    path('course/<str:role>/<int:id>', views.course, name='course'),

    path('aboutus/', views.aboutus, name='aboutus'),
    path('index', views.index, name='index'),
    path('courses', views.courses, name='courses'),

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout,name='logout'),

    path('profile/', views.profile, name='profile')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)