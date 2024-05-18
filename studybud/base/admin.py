from django.contrib import admin

# Register your models here.

from .models import Room

# this add the model Room to admin Panel
admin.site.register(Room)

