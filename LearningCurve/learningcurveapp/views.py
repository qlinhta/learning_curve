from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth import authenticate


def courses(request):
    return render(request, 'learningcurveapp/courses.html')


def index(request):
    return render(request, 'learningcurveapp/index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/learningcurveapp/profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        u = authenticate(username=username, password=password)
        print(u)
        if u:
            auth.login(request, u)
            return redirect('/learningcurveapp/profile')

    return render(request, 'learningcurveapp/login.html', context={
        'error_message': 'The username or password is wrong, Please retry',
    })


def student_path(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-path.html', context={
        'username': request.user.username,
    })


def student_profile(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-profile.html', context={
        'username': request.user.username,
    })


def student_quiz_result_details(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-quiz-result-details.html', context={
        'username': request.user.username,
    })


def student_quiz_results(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-quiz-results.html', context={
        'username': request.user.username,
    })


def student_take_course(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-course.html', context={
        'username': request.user.username,
    })


def student_take_lesson(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-lesson.html', context={
        'username': request.user.username,
    })


def student_take_quiz(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-quiz.html', context={
        'username': request.user.username,
    })


def teacher_profile(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-profile.html', context={
        'username': request.user.username,
    })


def teacher_addcourses(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-addcourses.html', context={
        'username': request.user.username,
    })


def teacher_mycourses(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-mycourses.html', context={
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
        profile_type = request.POST['profile_type']
        if User.objects.filter(username=username).first():
            messages.info(request, "The username is already taken, please try another username...")
            return render(request, 'learningcurveapp/signup.html', context={
                'error_message': "The username is already taken, please try another username...",
            })
        if 'agree' not in request.POST:
            messages.info(request, "You have to agree to create an account")
            return render(request, 'learningcurveapp/signup.html', context={
                'error_message': "You have to agree to create an account",
            })
        else:
            agree = request.POST['agree']
            user = User.objects.create_user(username=username, email=email, password=password)
            if (profile_type == 'Student'):
                my_group = Group.objects.get(name='student')
                my_group.user_set.add(user)

                auth.login(request, user)
                return redirect('/learningcurveapp/student-path')
            if (profile_type == 'Teacher'):
                my_group = Group.objects.get(name='teacher')
                my_group.user_set.add(user)
                auth.login(request, user)
                return redirect('/learningcurveapp/teacher-profile/')
    return render(request, 'learningcurveapp/signup.html')


def logout(request):
    if not request.user.is_authenticated:
        return render(request, 'learningcurveapp/login.html')
    auth.logout(request)
    return render(request, 'learningcurveapp/login.html')


def instructor_edit_quiz(request):
    return render(request, 'learningcurveapp/instructor-edit-quiz.html')