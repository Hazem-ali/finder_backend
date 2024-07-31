from django.contrib import admin

from .models import Suspect, SuspectPhoto


admin.site.register(Suspect)
admin.site.register(SuspectPhoto)