from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User,auth,Group
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import LEVELS, TOPIC
from .models import *


current_author=None
current_student=None




def courses(request):
    return render(request, 'learningcurveapp/courses.html')


def index(request):
    return render(request, 'learningcurveapp/index.html')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description','topic','difficulty']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title','description','number','content']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course',
                 ]

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

def teacher_addcourses(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-addcourses.html',context = {
        'username': request.user.username,
    })

def teacher_mycourses(request):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    return render(request, 'learningcurveapp/teacher-mycourses.html',context = {
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

    return render(request, 'learningcurveapp/teacher-mycourses.html',{'courses':courses})


@login_required
def teacher_addcourse(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')


    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            newcourse = form.save(commit=False)
            newcourse.author = author
            newcourse.save()
            courses=Course.objects.filter(author=author).values()
            return render(request, 'learningcurveapp/teacher-mycourses.html',{'courses':courses})

        else:
            return render(request, 'learningcurveapp/teacher-addcourse.html',{'form': CourseForm()})
    else:
        return render(request, 'learningcurveapp/teacher-addcourse.html',{'form': CourseForm()})


def teacher_course(request,id):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    author = Author.objects.get(user=request.user)
    course=Course.objects.get(id=id)
    chapters=Chapter.objects.filter(course=id).order_by('number').values()


    return render(request, 'learningcurveapp/course.html',{'teacher':True,'course':course,'chapters':chapters,'id':id})


@login_required
def teacher_addchapter(request,id):
    if request.method == 'POST':
        form = ChapterForm(request.POST,request.FILES)
        if form.is_valid():
            course=Course.objects.get(id=id)
            newchapter=form.save(commit=False)
            newchapter.course=course
            newchapter.save()

            return teacher_course(request,id)

        else:
            print(form.errors)

            return render(request, 'learningcurveapp/teacher-addchapter.html',{'id':id,'form': ChapterForm()})
    else:
        return render(request, 'learningcurveapp/teacher-addchapter.html',{'id':id,'form': ChapterForm()})

def instructor_edit_quiz(request):
    return render(request, 'learningcurveapp/instructor-edit-quiz.html')

@login_required
def chapter(request,id):
        chapter=Chapter.objects.get(id=id)
        print("chapter.content.url")
        print(chapter.content.url)
        return render(request, 'learningcurveapp/chapter.html',{'chapter':chapter})

def edit_account_profile(request):
    return render(request, 'learningcurveapp/edit-account-profile.html')

@login_required
def teacher_quizzes(request):
    author = Author.objects.get(user=request.user)
    quizz = Quiz.objects.filter(author=author).select_related()

    return render(request, 'learningcurveapp/teacher-quizzes.html',{'quizz':quizz})


@login_required
def teacher_addquizz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            newquiz=form.save(commit=False)
            newquiz.author=author
            newquiz.save()

            return teacher_quizzes(request)

        else:
            print(form.errors)

            return render(request, 'learningcurveapp/teacher-addquizz.html',{'form': QuizForm()})
    else:
        return render(request, 'learningcurveapp/teacher-addquizz.html',{'form': QuizForm()})

@login_required
def teacher_showquiz(request,id):
    quiz=Quiz.objects.get(id=id)
    return render(request, 'learningcurveapp/student-take-quiz.html',{'quiz':quiz})


@login_required
def teacher_coursefeedback(request,id):
    return render(request, 'learningcurveapp/coursefeedback.html',{'id':id})
