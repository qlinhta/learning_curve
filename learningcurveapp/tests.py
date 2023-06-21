
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Student, Course, Chapter,Quiz, Question, StudentQuiz, ChapterCompletion, CourseRate


# Create your tests here.
class DatabaseTest(TestCase):
    def setUp(self):
        self.userTeacher = User.objects.create(username='testuserTeacher')
        self.author = Author.objects.create(
            user=self.userTeacher,
            description='Test description',
            profile='author/test.jpg',
            facebook_link='',
            instagram_link=''
        )
        self.userStudent = User.objects.create(username='testuserStudent')
        self.student = Student.objects.create(
            user=self.userStudent,
            description='Test description',
            profile='student/test.jpg',
            points=100
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            author=self.author,
            topic='O',
            difficulty='B',
            subtitle='O'
        )
        self.chapter = Chapter.objects.create(
            title='Test Chapter',
            description='Test description',
            number=1,
            course=self.course,
            content='chapters/test.pdf',
            content_type='pdf',
            time=30
        )
        self.quiz = Quiz.objects.create(
            author=self.author,
            course=self.course
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question='Test question',
            answer='Test answer'
        )
        self.student_quiz = StudentQuiz.objects.create(
            student=self.student,
            points=100,
            quiz=self.quiz
        )
        self.chapter_completion = ChapterCompletion.objects.create(
            student=self.student,
            chapter=self.chapter
        )
        self.course_rate = CourseRate.objects.create(
            student=self.student,
            course=self.course,
            result=4,
            comments='Test comments'
        )                
        
    def test_author_str(self):
        self.assertEqual(str(self.author), self.userTeacher.username)

    def test_student_str(self):
        self.assertEqual(str(self.student), self.userStudent.username)
    def test_course_str(self):
        self.assertEqual(str(self.course), 'Test Course')
    def test_chapter_str(self):
        expected_str = "Chapter 1 of Test Course"
        self.assertEqual(str(self.chapter), expected_str)
    def test_quiz_str(self):
        expected_str = "Quiz Test Course"
        self.assertEqual(str(self.quiz), expected_str)
    def test_question_str(self):
        expected_str = f"Quiz {self.quiz.course}"
        self.assertEqual(str(self.question), expected_str)
    def test_student_quiz_str(self):
        expected_str = "Quiz Test Course"
        self.assertEqual(str(self.student_quiz), expected_str)
    def test_chapter_completion_str(self):
        expected_str = "Student testuserStudent"
        self.assertEqual(str(self.chapter_completion), expected_str)
    def test_course_rate_str(self):
        expected_str = "Student testuserStudent"
        self.assertEqual(str(self.course_rate), expected_str)