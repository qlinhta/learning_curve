# Generated by Django 4.1.7 on 2023-06-19 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningcurveapp', '0004_alter_chapter_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='facebook_link',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='author',
            name='instagram_link',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='student',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
