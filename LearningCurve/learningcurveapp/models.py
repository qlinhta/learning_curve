from django.db import models
from django.contrib.auth.models import User


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




class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='courses')

    topic = models.CharField(choices=TOPIC, max_length=10, default='O')
    difficulty = models.CharField(choices=LEVELS, max_length=1, default='B')

    def __str__(self) -> str:
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    number = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content= models.FileField(max_length=1000, default='')








class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz')

    def __str__(self) -> str:
        return "Quiz " + self.course.__str__()


class QuizCompletion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="quiz_completions")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_completions")
    result = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__() + "Student " + self.student

class CourseCompletion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course_completions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_completions")
    result = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__() + "Student " + self.student


class CourseRates(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course_rate")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_rate")
    result = models.PositiveSmallIntegerField()
    comments = models.TextField()

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__() + "Student " + self.student


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    number = models.PositiveSmallIntegerField()
    question = models.TextField()

    def __str__(self) -> str:
        return "Quiz " + self.quiz.course.__str__() + "Question " + self.number


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_true = models.BooleanField()
    text = models.CharField(max_length=150)

    def __str__(self) -> str:
        return "Quiz " + self.question.quiz.course.__str__() + " - Question " + self.question.number + " - " + self.text

