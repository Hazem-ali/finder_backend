# Generated by Django 3.1.7 on 2024-07-26 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder_app', '0006_auto_20240725_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='suspectphoto',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='suspect_photos/'),
        ),
    ]