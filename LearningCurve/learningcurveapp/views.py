from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms


def login(request):
    return render(request, 'learningcurveapp/login.html')


def student_path(request):
    return render(request, 'learningcurveapp/student-path.html')


def teacher_profile(request):
    return render(request, 'learningcurveapp/teacher-profile.html')


def aboutus(request):
    return render(request, 'learningcurveapp/aboutus.html')
