from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User,auth,Group
from django.contrib.auth.decorators import login_required

from django.db.models import Prefetch
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import LEVELS, TOPIC
from .models import *
from django.shortcuts import redirect, reverse
from django.db.models import Sum, Avg, Max,Count
from fuzzywuzzy import fuzz


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description','topic','difficulty']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title','description','number','content','content_type','time']
        widgets = {
                            'title':forms.TextInput(attrs={'class':"form-control"}),
                            'description': forms.Textarea(attrs={'blank':'true','class':"form-control",'rows':"3",'placeholder':"Present your course"}),
                            'number':forms.NumberInput(attrs={'class':"form-control"}),
                            'content':forms.FileInput(attrs={'class':"custom-file"}),
                        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].required = False

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer']

class CourseRateForm(forms.ModelForm):

    class Meta:
        model = CourseRate
        fields = ['result', 'comments']
        widgets = {
                    'comments': forms.Textarea(attrs={'blank':'true','class':"form-control",'rows':"3",'placeholder':"Can you give a comments..."}),
                    'result':forms.NumberInput(attrs={'class':"form-control"}),
                                }

class FilterForm(forms.Form):
    level = forms.ChoiceField(choices=LEVELS_CHOICE, required=False, initial='')
    topic = forms.ChoiceField(choices=TOPIC_CHOICE, required=False, initial='')


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model=Author
        fields = ['profile','description','facebook_link','instagram_link']
        widgets = {
            'description': forms.Textarea(attrs={'blank':'true','class':"form-control",'rows':"3",'placeholder':"Present yourself"}),
            'profile': forms.FileInput(attrs={'blank':'true','class':"custom-file"}),
            'facebook_link':forms.TextInput(attrs={'blank':'true','class':"form-control"}),
            'instagram_link':forms.TextInput(attrs={'blank':'true','class':"form-control"}),
        }

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = ['profile','description']
        widgets = {
            'description': forms.Textarea(attrs={'class':"form-control",'rows':"3",'placeholder':"Present yourself"}),
            'profile': forms.FileInput(attrs={'class':"custom-file"}),
        }


def index(request):
    return render(request, 'learningcurveapp/index.html')

def courses(request):
    return render(request, 'learningcurveapp/courses.html')



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

@login_required
def student_profile(request):

    current_student=request.user
    student = Student.objects.get(user__username=current_student.username)
    cours_lus = ChapterCompletion.objects.filter(student=student)
    nombre_chapitre_lus = cours_lus.count()
    quiz_answered = StudentQuiz.objects.filter(student = student).count()
    if quiz_answered == 0:
        average_grade = 0
        max_grade = 0
        max_course = ""
        course_to_continue = Course.objects.get(id=1)
        avancement = "0/" +str(student.course_completions_student.filter(chapter__course=course_to_continue).count())
    else:
        average  = StudentQuiz.objects.filter(student = student).aggregate(Avg('points'))['points__avg']
        average_grade = round(average, 2)
        max_grade =  StudentQuiz.objects.filter(student=student).aggregate(max_score=Max('points'))['max_score']
        max_course =  StudentQuiz.objects.filter(student=student, points=max_grade).first().quiz.course
        to_continue = False
        read_courses = ChapterCompletion.objects.filter(student = student)
        to_continue = False
        for i in read_courses:
            c = i.chapter.course
            isComplete, avancement = isCompleted(c, student)
            if not isComplete:
                to_continue = True
                course_to_continue = c
                print(avancement)
                break
        if not to_continue:
            course_to_continue = Course.objects.get(id=1)
            avancement = "0/" +str(student.course_completions_student.filter(chapter__course=course_to_continue).count())
    return render(request, 'learningcurveapp/student-profile.html',context = {
        'username': request.user.username,
        'read_chapters': nombre_chapitre_lus,
        'answered_quiz':quiz_answered,
        'average_grade': average_grade,
        'max_grade': max_grade,
        'max_course': max_course,
        'course_to_continue': course_to_continue,
        'advancement': avancement
    })

def isCompleted(c, student):
    chapitres_total = Chapter.objects.filter(course=c).count()
    chapitres_completes = student.course_completions_student.filter(chapter__course=c).count()
    print(chapitres_total, chapitres_completes)
    return chapitres_completes == chapitres_total, str(chapitres_completes)+"/"+str(chapitres_total)


def student_quiz_result_details(request,id):
    if not request.user.is_authenticated:
        return redirect('/learningcurveapp/login')
    questions=Question.objects.filter(quiz=id).order_by('id').values()
    if request.method == 'POST':
        i=0
        result=0
        answer_list = request.POST.getlist('answer[]')
        for q in questions:
            if fuzz.token_set_ratio(q['answer'], answer_list[i])>90:
                result=result+1
            i=i+1
        student = Student.objects.get(user=request.user)
        quiz=Quiz.objects.get(id=id)
        studentquiz=StudentQuiz(student=student,quiz=quiz,points=result)
        studentquiz.save()
        best_score_perso = StudentQuiz.objects.filter(quiz=quiz, student=student).aggregate(max_score=Max('points'))['max_score']
        best_score = StudentQuiz.objects.filter(quiz=quiz).aggregate(max_score=Max('points'))['max_score']

    return render(request, 'learningcurveapp/student-quiz-result-details.html',context = {'quiz':quiz,'id':id,
     'username': request.user.username,'questions':questions,'role':'student',
     'result':result,'total':len(answer_list),'best_score_perso':best_score_perso,'best_score':best_score})


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

    current_teacher = request.user
    courses = Course.objects.filter(author__user=current_teacher)
    chapter_counts = {}
    average_rates = {}

    quizzes = 0
    answered_quizzes = 0 
    average_scores_quizz = overall_average_score = CourseRate.objects.filter(course__in=courses).aggregate(Avg('result'))
    for course in courses:
        chapter_count = Chapter.objects.filter(course=course).count()
        chapter_counts[course] = chapter_count
        average_rate = CourseRate.objects.filter(course=course).aggregate(Avg('result'))
        average_rates[course] = average_rate['result__avg']

        quizzes = quizzes+ Quiz.objects.filter(course=course).count()
        answered_quizzes += StudentQuiz.objects.filter(quiz__course=course, student__user=current_teacher).count()
    

    return render(request, 'learningcurveapp/teacher-profile.html', context={
        'username': request.user.username,
        'courses': courses,
        'chapter_counts': chapter_counts,
        'average_rates': average_rates,
        'quizzes' : quizzes,
        'answered_quizzes': answered_quizzes,
        'average_scores_quizz':average_scores_quizz['result__avg'],
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
    return render(request, 'learningcurveapp/personal_courses.html',context = {
        'username': request.user.username,
    })





@login_required
def profile(request):
    user = request.user
    group=user.groups.first().name
    print(group)
    if group=='teacher':
        return redirect('/learningcurveapp/teacher-profile')
    if group=='student' :
        return redirect('/learningcurveapp/student-profile')
    else:
        return redirect('/learningcurveapp/teacher-profile')




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
                return redirect('/learningcurveapp/student-profile')
            if(profile_type=='Teacher'):
                my_group = Group.objects.get(name='teacher')
                my_group.user_set.add(user)
                auth.login(request,user)
                author=Author(user=user)
                author.save()
                current_author=author

                return redirect('/learningcurveapp/teacher-profile/')
    return render(request, 'learningcurveapp/signup.html')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'learningcurveapp/login.html')

@login_required
def teacher_addcourse(request):
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

            url = reverse('course', args=(id,))
            return redirect(url)

        else:
            print(form.errors)

            return render(request, 'learningcurveapp/teacher-editchapter.html',context ={'value':'teacher-addchapter','id':id,'form': ChapterForm()})
    else:
        return render(request, 'learningcurveapp/teacher-editchapter.html',context ={'value':'teacher-addchapter','id':id,'form': ChapterForm()})

@login_required
def instructor_edit_quiz(request):
    return render(request, 'learningcurveapp/instructor-edit-quiz.html')

@login_required
def chapter(request,id):
    role=request.user.groups.first().name
    chapter=Chapter.objects.get(id=id)
    chapter_completed=False
    if(role=='student'):
        student = Student.objects.get(user=request.user)
        chapter_completed = ChapterCompletion.objects.filter(chapter=chapter, student=student).exists()
    return render(request, 'learningcurveapp/chapter.html',context ={'chapter':chapter,'role':role,'chapter_completed':chapter_completed,'id':chapter.course_id})

@login_required
def edit_account_profile(request):
    group=request.user.groups.first().name
    if(group=='teacher'):
        if (request.method == 'POST'):
            form=AuthorUpdateForm(request.POST,request.FILES,instance=Author.objects.get(user=request.user))
            if form.is_valid():
                form.save()
        return render(request, 'learningcurveapp/edit-account-profile.html',context ={'id':id,'form': AuthorUpdateForm()})
    if(group=='student'):
        if (request.method == 'POST'):
            form=StudentUpdateForm(request.POST,request.FILES,instance=Student.objects.get(user=request.user))
            if form.is_valid():
                form.save()
        return render(request, 'learningcurveapp/edit-account-profile.html',context ={'id':id,'form': StudentUpdateForm()})
    return render(request, 'learningcurveapp/index.html')


@login_required
def quizzes(request):
    role=request.user.groups.first().name
    if(role=="teacher"):
        author = Author.objects.get(user=request.user)
        quizz = Quiz.objects.filter(author=author).select_related()
    if(role=="student"):
       quizz = Quiz.objects.all()
    return render(request, 'learningcurveapp/quizzes.html',{'quizz':quizz,'role':role})



@login_required
def student_quizzes(request):
        quizz = Quiz.objects.all()
        return render(request, 'learningcurveapp/quizzes.html',{'quizz':quizz,'role':"student"})



@login_required
def teacher_addquizz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            quiz = form.save(commit=False)
            quiz.author=author
            quiz.save()

            i = 0
            has_question_form = True
            while has_question_form:
                question_form = QuestionForm(request.POST, prefix=f'question_{i}')
                if question_form.is_valid():
                    question = question_form.save(commit=False)
                    question.quiz = quiz
                    question.save()
                    i += 1
                else:
                    has_question_form = False

            return teacher_quizzes(request)

    else:
        return render(request, 'learningcurveapp/teacher-addquizz.html',{'form': QuizForm()})




@login_required
def coursefeedback(request,id):
    role=request.user.groups.first().name
    course=Course.objects.get(id=id)
    course_rates = CourseRate.objects.filter(course=course)
    response=False
    if(role=='student'):
        student = Student.objects.get(user=request.user)
        course= Course.objects.get(id=id)
        response = CourseRate.objects.filter(student=student, course=course).exists()
    return render(request, 'learningcurveapp/coursefeedback.html',{'course_rates':course_rates,'course':course,'role':role,'form':CourseRateForm(),'response':response})


def teacher_mycourses(request):
    if not request.user.is_authenticated:
        return redirect('learningcurveapp/login')
    author = Author.objects.get(user=request.user)
    courses=Course.objects.filter(author=author).values()

    return render(request, 'learningcurveapp/private-courses.html',{'courses':courses})


@login_required
def student_courses(request):
    courses = Course.objects.all()
    return render(request, 'learningcurveapp/private-courses.html',{'courses':courses,'role':'role','form':FilterForm()})


@login_required
def private_courses(request):
    role=request.user.groups.first().name
    courses=Course.objects.select_related('chapter_course').all()
    courses=courses.select_related('course_rate').all()
    courses= courses.annotate(
                                total_chapters=Count('chapter_course', distinct=True),
                                total_time=Sum('chapter_course__time', distinct=True),
                                average_result=Avg('course_rate__result')

                            ).values('id','title', 'total_chapters', 'total_time', 'average_result', 'difficulty','topic')
    if request.method == 'POST':
            form = FilterForm(request.POST)
            if form.is_valid():
                level = request.POST['level']
                topic = request.POST['topic']
                if(level!='' and topic!=''):

                    courses = Course.objects.filter(difficulty=level, topic=topic).annotate(
                        total_chapters=Sum('chapter_course__number'),
                        total_time=Sum('chapter_course__time'),
                        average_result=Avg('course_rate__result')
                    ).values('id','title', 'total_chapters', 'total_time', 'average_result', 'difficulty','topic')

                if(topic=='' and level!=''):
                      courses = Course.objects.filter(difficulty=level).annotate(
                                             total_chapters=Sum('chapter_course__number'),
                                             total_time=Sum('chapter_course__time'),
                                             average_result=Avg('course_rate__result')
                        ).values('id','title', 'total_chapters', 'total_time', 'average_result', 'difficulty','topic')
                if(topic!='' and level==''):
                     courses = Course.objects.filter(topic=topic).annotate(
                                            total_chapters=Sum('chapter_course__number'),
                                            total_time=Sum('chapter_course__time'),
                                            average_result=Avg('course_rate__result')
                                        ).values('id','title', 'total_chapters', 'total_time', 'average_result', 'difficulty','topic')
    return render(request, 'learningcurveapp/private-courses.html',{'courses':courses,'role':role,'form':FilterForm()})





@login_required
def edit_account_profile(request):
    group=request.user.groups.first().name
    if(group=='teacher'):
        if (request.method == 'POST'):
            form=AuthorUpdateForm(request.POST,request.FILES,instance=Author.objects.get(user=request.user))
            if form.is_valid():
                form.save()
        return render(request, 'learningcurveapp/edit-account-profile.html',context ={'id':id,'form': AuthorUpdateForm()})
    if(group=='student'):
        if (request.method == 'POST'):
            form=StudentUpdateForm(request.POST,request.FILES,instance=Student.objects.get(user=request.user))
            if form.is_valid():
                form.save()
        return render(request, 'learningcurveapp/edit-account-profile.html',context ={'id':id,'form': StudentUpdateForm()})
    return render(request, 'learningcurveapp/index.html')


@login_required
def showquiz(request,id):
    role=request.user.groups.first().name
    questions=Question.objects.filter(quiz=id).order_by('id').values()
    return render(request, 'learningcurveapp/showquiz.html',{'id':id,'questions':questions,'role':role})

@login_required
def course(request,id):
    role=request.user.groups.first().name
    review_count = 0
    review_avg = 0
    chapter_completes=None
    progression=0
    time=0
    course=Course.objects.get(id=id)
    chapters=Chapter.objects.filter(course=id).order_by('number').values()
    others_course=Course.objects.filter(author=course.author)[:3]
    course_rates = CourseRate.objects.filter(course=course)
    quizzes = Quiz.objects.filter(course_id=id)
    if(course_rates.count()!=0):
        review_count = CourseRate.objects.filter(course_id=id).count()
        review_avg = CourseRate.objects.filter(course=course).aggregate(Avg('result'))['result__avg']
    if(chapters.count()!=0):
        time=chapters.aggregate(total_duree=models.Sum('time'))['total_duree']
        if( role=='student' ):
            student = Student.objects.get(user=request.user)
            chapter_completes = set(student.course_completions_student.filter(chapter__course=course).values_list('chapter_id', flat=True))
            progression=int(len(chapter_completes)/chapters.count()*100)


    return render(request, 'learningcurveapp/course.html',{'role':role,'course':course,'chapters':chapters,'time':time, 'quizzes':quizzes,
                                                            'course_rates':course_rates,'others_course':others_course,
                                                             'review_count':review_count,'review_avg':review_avg,'chapter_completes':chapter_completes,
                                                             'progression':progression, 'total_chapters':chapters.count()})


@login_required
def student_chapter_complete(request,id):
    chapter=Chapter.objects.get(id=id)
    student = Student.objects.get(user=request.user)
    chaptercompletion=ChapterCompletion(chapter=chapter,student=student)
    chaptercompletion.save()
    url = reverse('course', args=(chapter.course.id,))

    return redirect(url)


@login_required
def student_feedback(request,id):
    if request.method == 'POST':
            form = CourseRateForm(request.POST)
            if form.is_valid():
                student = Student.objects.get(user=request.user)
                course= Course.objects.get(id=id)
                feedback = form.save(commit=False)
                feedback.student=student
                feedback.course=course
                feedback.save()
    url = reverse('coursefeedback', args=(id,))
    return redirect(url)


@login_required
def teacher_edit_chapter(request,id):
    if request.method == 'POST':
        form = ChapterForm(request.POST,request.FILES,instance=Chapter.objects.get(id=id))
        if form.is_valid():
             form.save()
             #('course/'+str()Chapter.objects.get(id=id).course_id)
             url = reverse('course', args=(Chapter.objects.get(id=id).course_id,))
             return redirect(url)

    return render(request, 'learningcurveapp/teacher-editchapter.html',context ={'value':'teacher-edit-chapter','id':id,'form': ChapterForm()})
