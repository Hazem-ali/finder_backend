# Generated by Django 3.1.7 on 2024-09-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_auto_20240827_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
