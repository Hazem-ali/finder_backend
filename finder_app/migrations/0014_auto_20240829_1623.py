# Generated by Django 3.1.7 on 2024-08-29 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finder_app', '0013_auto_20240827_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='photo',
            new_name='image',
        ),
    ]
