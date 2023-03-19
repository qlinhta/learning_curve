from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django import forms


def login(request):
    return render(request, 'learningcurveapp/login.html')


def student_path():
    return render(request, 'learningcurveapp/student-path.html')


def teacher_profile():
    return render(request, 'learningcurveapp/teacher-profile.html')
