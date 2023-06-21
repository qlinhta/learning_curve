from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Quiz)
admin.site.register(ChapterCompletion)
admin.site.register(Question)
admin.site.register(StudentQuiz)
admin.site.register(CourseRate)

# Register your models here.
