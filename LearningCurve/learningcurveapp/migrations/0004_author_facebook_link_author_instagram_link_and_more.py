# Generated by Django 4.1.7 on 2023-06-21 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("learningcurveapp", "0003_chaptercompletion_courserate_studentquiz_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="facebook_link",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="author",
            name="instagram_link",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="student",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="author",
            name="profile",
            field=models.ImageField(null=True, upload_to="author/"),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="content",
            field=models.FileField(default="", max_length=1000, upload_to="chapters/"),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chapter_course",
                to="learningcurveapp.course",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="profile",
            field=models.ImageField(null=True, upload_to="student/"),
        ),
    ]
