from django.db import models
from django.contrib.auth.models import User


LEVELS = (
    ('I', 'Introduction'),
    ('B', 'Beginner'),
    ('M', 'Medium'),
    ('C', 'Confirmed'),
    ('E', 'Expert')
)


TEXT_FORMAT = (
    ('Mark', 'Markdown'),
    ('Lat', 'Latex'),
    ('HTML', 'HTML'),
    ('Text', 'Text'),
)


LINK_FORMAT = (
    ('Vid', 'Video'),
    ('Lin', 'Link'),
    ('Pic', 'Picture'),
    ('Pdf', 'PDF')
)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Field(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=25)
    field = models.ManyToManyField(Field, related_name='topics')

    def __str__(self) -> str:
        return self.field.__str__() + " - " + self.name


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='courses')

    field = models.ManyToManyField(Field, related_name='fields')
    topic = models.ManyToManyField(Topic, related_name='courses')
    difficulty = models.CharField(choices=LEVELS, max_length=1)

    def __str__(self) -> str:
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.course.__str__() + " Chapter " + self.number


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=150)
    number = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.chapter.__str__() + " - Paragraph " + self.number


class Text(models.Model):
    text = models.TextField()
    type = models.CharField(choices=TEXT_FORMAT, max_length=3),
    index = models.PositiveSmallIntegerField()
    paragraph = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="texts")


class Link(models.Model):
    link = models.CharField(max_length=200)
    type = models.CharField(choices=LINK_FORMAT, max_length=3)
    index = models.PositiveSmallIntegerField()
    paragraph = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="links")


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

