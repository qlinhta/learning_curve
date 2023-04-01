from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User





def login(request):
    return render(request, 'learningcurveapp/login.html', {
                'form': forms.Authentication()
            })


def student_path(request):
    return render(request, 'learningcurveapp/student-path.html')


def teacher_profile(request):
    return render(request, 'learningcurveapp/teacher-profile.html')


def aboutus(request):
    return render(request, 'learningcurveapp/aboutus.html')

isConnect = False
def enter_login(request):
    global isConnect
    if isConnect:
        return render(request, 'learningcurveapp/student-path.html')
    if request.method == 'POST':
        name = request.POST['username']
        pswd = request.POST['password']
        user = authenticate(username=name, password=pswd)

        if user is not None:
            isConnect = True
            return render(request, 'learningcurveapp/student-path.html')
        else:
            return render(request, 'learningcurveapp/login.html')

def signingup(request):
    global isConnect
    if isConnect:
        return render(request, 'learningcurveapp/student-path.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(username=username,email=email, password=password)
        return render(request, 'learningcurveapp/student-path.html')

def signup(request):
    return render(request, 'learningcurveapp/signup.html')






