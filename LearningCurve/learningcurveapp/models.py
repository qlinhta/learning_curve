from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



LEVELS = (
    ('I', 'Introduction'),
    ('B', 'Beginner'),
    ('M', 'Medium'),
    ('C', 'Confirmed'),
    ('E', 'Expert')
)

TOPIC = (
    ( 'CS','Computer sciences'),
    ('F','Finance'),
    ('S','Social'),
    ('O','Others'),

)

LEVELS_CHOICE = (
    ('', ''),
    ('I', 'Introduction'),
    ('B', 'Beginner'),
    ('M', 'Medium'),
    ('C', 'Confirmed'),
    ('E', 'Expert')
)

TOPIC_CHOICE = (
    ('', ''),
    ( 'CS','Computer sciences'),
    ('F','Finance'),
    ('S','Social'),
    ('O','Others'),

)

TYPE = (
         ( 'mp4','mp4'),
         ('mp3','mp3'),
         ('pdf','pdf'),
         ('jpg','jpg'),
         ('png','png'),

     )




class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField( default='')
    profile=models.ImageField(null=True)
    def __str__(self) -> str:
            return  self.user.__str__()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile=models.ImageField(null=True)
    points = models.PositiveSmallIntegerField( default=0)

    def __str__(self) -> str:
            return  self.user.__str__()


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='course_author')

    topic = models.CharField(choices=TOPIC, max_length=10, default='O')
    difficulty = models.CharField(choices=LEVELS, max_length=1, default='B')
    subtitle = models.CharField(max_length=300, default='O')

    def __str__(self) -> str:
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='chapter_course')
    content= models.FileField(max_length=1000, default='')
    content_type = models.CharField(choices=TYPE, max_length=10, default='pdf')
    time = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],default=0)

    def __str__(self) -> str:
        return "Chapter " + str(self.number) + " of "+ self.course.__str__()





class Quiz(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='related_author',default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='related_course',null=True)


    def __str__(self) -> str:
        return "Quiz " + self.course.__str__()




class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(default='')
    answer = models.CharField(max_length=150, default='')
    answer=models.CharField(max_length=150,default='')

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__()



class StudentQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentquiz_student",default='')
    points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="studentquiz")

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__()


class ChapterCompletion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course_completions_student",default='')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="course_completions_course",default='')


    def __str__(self) -> str:
        return "Student " + self.student.__str__()


class CourseRate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course_rate_student",default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_rate",default='')
    result = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comments = models.TextField()

    def __str__(self) -> str:
        return "Student " + self.student.__str__()


