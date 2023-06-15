from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User,auth,Group
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import LEVELS, TOPIC
from .models import *


current_author=None
current_student=None
class NewContent(forms.Form):
    name = forms.CharField(label='Name',max_length=20)
    topics = forms.ChoiceField(choices=TOPIC)
    level = forms.ChoiceField(choices=LEVELS)
    description = forms.CharField(label='description')


class NewChapter(forms.Form):
    name = forms.CharField(label='Name',max_length=20)
    number = forms.IntegerField(label='number')
    description = forms.CharField(label='description')
    content = forms.FileField(label='file')

def login(request):

    if request.user.is_authenticated:
        return redirect('/learningcurveapp/profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        u = authenticate(username=username, password=password)
        print(u)
        if u:
            auth.login(request,u)
            return redirect('/learningcurveapp/profile')


    return render(request, 'learningcurveapp/login.html', context = {
        'error_message': 'The username or password is wrong, Please retry',
    } )


def student_path(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-path.html',context = {
        'username': request.user.username,
    })

def student_profile(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    current_student=request.user
    return render(request, 'learningcurveapp/student-profile.html',context = {
        'username': request.user.username,
    })

def student_quiz_result_details(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-quiz-result-details.html',context = {
        'username': request.user.username,
    })
def student_quiz_results(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-quiz-results.html',context = {
        'username': request.user.username,
    })

def student_take_course(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-course.html',context = {
        'username': request.user.username,
    })

def student_take_lesson(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-lesson.html',context = {
        'username': request.user.username,
    })
def student_take_quiz(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/student-take-quiz.html',context = {
        'username': request.user.username,
    })

def teacher_profile(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    current_author=request.user
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
            return render(request, 'learningcurveapp/signup.html',context = {
                'error_message': "The username is already taken, please try another username...",
            })
        if 'agree'  not in request.POST:
            messages.info(request,"You have to agree to create an account")
            return render(request, 'learningcurveapp/signup.html',context = {
                'error_message': "You have to agree to create an account",
            })
        else:
            agree=request.POST['agree']
            user=User.objects.create_user(username=username,email=email, password=password)
            if(profile_type=='Student'):
                my_group = Group.objects.get(name='student')
                my_group.user_set.add(user)

                auth.login(request,user)
                student=Student(user=user)
                student.save()
                current_student=student
                return redirect('/learningcurveapp/student-path')
            if(profile_type=='Teacher'):
                my_group = Group.objects.get(name='teacher')
                my_group.user_set.add(user)
                auth.login(request,user)
                author=Author(user=user)
                author.save()
                current_author=author

                return redirect('/learningcurveapp/teacher-profile/')
    return render(request, 'learningcurveapp/signup.html')



def logout(request):
    if not request.user.is_authenticated:
        return render(request, 'learningcurveapp/login.html')
    auth.logout(request)
    current_author=None
    current_student=None
    return render(request, 'learningcurveapp/login.html')



def teacher_mycourses(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    author = Author.objects.get(user=request.user)
    courses=Course.objects.filter(author=author).values()
    print(courses)
    return render(request, 'learningcurveapp/teacher_mycourses.html',{'courses':courses})

def teacher_addcourse(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    author = Author.objects.get(user=request.user)

    if request.method == 'POST':
        form = NewContent(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].title()
            topic = form.cleaned_data['topics']
            level= form.cleaned_data['level']
            description= form.cleaned_data['description']



            print(author)
            newCourse=Course(author=author,title=name,description=description,topic=topic,difficulty=level)
            newCourse.save()
            print(newCourse)
            courses=Course.objects.filter(author=author).values()
            return render(request, 'learningcurveapp/teacher_mycourses.html',{'courses':courses})

        else:
            return render(request, 'learningcurveapp/teacher_addcourse.html',{'form': NewContent()})
    else:
        return render(request, 'learningcurveapp/teacher_addcourse.html',{'form': NewContent()})
def teacher_course(request,id):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    author = Author.objects.get(user=request.user)
    chapters=Chapter.objects.filter(course=id).order_by('number').values()


    return render(request, 'learningcurveapp/teacher_course.html',{'id':id,'chapters':chapters})


def teacher_addchapter(request,id):
    print("----------------------------------------------------------")
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')


    if request.method == 'POST':
        print("----------------------------------------------------------")
        form = NewChapter(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].title()
            number= form.cleaned_data['number']
            description= form.cleaned_data['description']
            file = request.FILES['content']
            course=Course.objects.get(id=id)
            print("---------------courses crée-----------------")
            print(course.id)
            newchapter=Chapter(course=course,title=name,number=number,description=description,content=file)
            newchapter.save()
            filename="static/Contents/"+str(newchapter.id)+file.name
            print(filename)
            with open(filename, "wb+") as destination:
                print("---------------fichier ouvert-----------------")
                for chunk in file.chunks():
                    destination.write(chunk)
            return teacher_course(request,id)

        else:
            print('form non valid')
            return render(request, 'learningcurveapp/teacher_addchapter.html',{'id':id,'form': NewChapter()})
    else:
        return render(request, 'learningcurveapp/teacher_addchapter.html',{'id':id,'form': NewChapter()})
