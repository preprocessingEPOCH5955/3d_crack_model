# Generated by Django 5.1.2 on 2024-10-29 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_signup_form_data_time_signup_form_face'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup_form',
            name='face',
        ),
        migrations.AddField(
            model_name='project_data',
            name='face',
            field=models.CharField(blank=True, default='F', max_length=10),
        ),
        migrations.AlterField(
            model_name='signup_form',
            name='data_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
