from django.db import models
from user_app.models import User

# Create your models here.


class Suspect(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    # TODO remove null=True in informer
    informer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="informer")

    where = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    national_id = models.CharField(max_length=14)


class SuspectPhoto(models.Model):
    # DONE change photo type to be imagefield
    photo = models.ImageField(upload_to="suspect_photos/", blank=True, null=True)
    # photo = models.CharField(max_length=255, blank=True, null=True)
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, related_name="photos")
    created_at = models.DateTimeField(auto_now_add=True)
