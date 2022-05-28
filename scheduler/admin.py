from django.contrib import admin
from .models import TimeSlot

admin.sites.site.register(TimeSlot)