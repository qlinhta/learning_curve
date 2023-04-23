# Generated by Django 4.1.7 on 2023-04-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningcurveapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='field',
        ),
        migrations.AddField(
            model_name='topic',
            name='field',
            field=models.ManyToManyField(related_name='topics', to='learningcurveapp.field'),
        ),
    ]
