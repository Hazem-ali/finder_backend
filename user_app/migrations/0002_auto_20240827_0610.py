# Generated by Django 3.1.7 on 2024-08-27 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='national_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
    ]
