from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User,auth,Group
from django.contrib import messages



def login(request):
    return render(request, 'learningcurveapp/login.html', {
                'form': forms.Authentication()
            })


def student_path(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-path.html',context = {
        'username': request.user.username,
    })


def teacher_profile(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-profile.html',context = {
        'username': request.user.username,
    })


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')

    user = request.user
    user = request.user
    teacher_group = Group.objects.filter(name='teacher').first()
    is_teacher = teacher_group in user.groups.all()
    if user.groups.filter(name='teacher').exists():
        return redirect('/learningcurveapp/teacher-profile')
    if user.groups.filter(name='student').exists():
        return redirect('/learningcurveapp/student-path')
    else:
        return redirect('/learningcurveapp/login')



def aboutus(request):
    return render(request, 'learningcurveapp/aboutus.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/learningcurveapp/profile')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        profile_type=request.POST['profile_type']
        if User.objects.filter(username=username).first():
            messages.info(request,"The username is already taken, please try another username...")
            return render(request, 'learningcurveapp/signup.html')
        if 'agree'  not in request.POST:
            messages.info(request,"You have to agree to create an account")
            return render(request, 'learningcurveapp/signup.html')
        else:
            agree=request.POST['agree']
            user=User.objects.create_user(username=username,email=email, password=password)
            if(profile_type=='Student'):
                my_group = Group.objects.get(name='student')
                my_group.user_set.add(user)

                auth.login(request,user)
                return redirect('/learningcurveapp/student-path')
            if(profile_type=='Teacher'):
                my_group = Group.objects.get(name='teacher')
                my_group.user_set.add(user)
                auth.login(request,user)
                return redirect('/learningcurveapp/teacher-profile/')
    return render(request, 'learningcurveapp/signup.html')



def logout(request):
    if not request.user.is_authenticated:
        return render(request, 'learningcurveapp/login.html')
    auth.logout(request)
    return render(request, 'learningcurveapp/login.html')





