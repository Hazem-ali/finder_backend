from django.contrib import admin

from .models import Contact, StatusHistory


admin.site.register(Contact)
admin.site.register(StatusHistory)