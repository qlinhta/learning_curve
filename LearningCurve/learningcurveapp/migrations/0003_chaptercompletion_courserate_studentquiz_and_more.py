# Generated by Django 4.1.7 on 2023-06-18 10:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learningcurveapp', '0002_remove_topic_field_topic_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.RemoveField(
            model_name='link',
            name='paragraph',
        ),
        migrations.RemoveField(
            model_name='quizcompletion',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizcompletion',
            name='student',
        ),
        migrations.RemoveField(
            model_name='section',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='text',
            name='paragraph',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='field',
        ),
        migrations.RemoveField(
            model_name='course',
            name='field',
        ),
        migrations.RemoveField(
            model_name='question',
            name='number',
        ),
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='author',
            name='profile',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='chapter',
            name='content',
            field=models.FileField(default='', max_length=1000, upload_to=''),
        ),
        migrations.AddField(
            model_name='chapter',
            name='content_type',
            field=models.CharField(choices=[('mp4', 'mp4'), ('mp3', 'mp3'), ('pdf', 'pdf'), ('jpg', 'jpg'), ('png', 'png')], default='pdf', max_length=10),
        ),
        migrations.AddField(
            model_name='chapter',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='chapter',
            name='time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='course',
            name='subtitle',
            field=models.CharField(default='O', max_length=300),
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='related_author', to='learningcurveapp.author'),
        ),
        migrations.AddField(
            model_name='student',
            name='points',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='profile',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='number',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_author', to='learningcurveapp.author'),
        ),
        migrations.AlterField(
            model_name='course',
            name='difficulty',
            field=models.CharField(choices=[('I', 'Introduction'), ('B', 'Beginner'), ('M', 'Medium'), ('C', 'Confirmed'), ('E', 'Expert')], default='B', max_length=1),
        ),
        migrations.RemoveField(
            model_name='course',
            name='topic',
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_course', to='learningcurveapp.course'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Field',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.DeleteModel(
            name='QuizCompletion',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AddField(
            model_name='studentquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentquiz', to='learningcurveapp.quiz'),
        ),
        migrations.AddField(
            model_name='studentquiz',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='studentquiz_student', to='learningcurveapp.student'),
        ),
        migrations.AddField(
            model_name='courserate',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='course_rate', to='learningcurveapp.course'),
        ),
        migrations.AddField(
            model_name='courserate',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='course_rate_student', to='learningcurveapp.student'),
        ),
        migrations.AddField(
            model_name='chaptercompletion',
            name='chapter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='course_completions_course', to='learningcurveapp.chapter'),
        ),
        migrations.AddField(
            model_name='chaptercompletion',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='course_completions_student', to='learningcurveapp.student'),
        ),
        migrations.AddField(
            model_name='course',
            name='topic',
            field=models.CharField(choices=[('CS', 'Computer sciences'), ('F', 'Finance'), ('S', 'Social'), ('O', 'Others')], default='O', max_length=10),
        ),
    ]
