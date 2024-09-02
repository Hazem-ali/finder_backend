from django.db import models
from user_app.models import User

# Create your models here.


class Contact(models.Model):

    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=14, unique=True)
    father = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children_of_father",
        blank=True,
        null=True,
    )
    mother = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children_of_mother",
        blank=True,
        null=True,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="contact_photos/", blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True)
    gender = models.CharField(max_length=1, null=True)
    status = models.CharField(max_length=255, null=True)
    status_last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.name:
            return f"{self.national_id} ({self.name})"
        return f"{self.national_id}"


class StatusHistory(models.Model):

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
