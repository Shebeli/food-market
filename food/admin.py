from django.contrib import admin
from .models import TheFood, SiteUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(TheFood)
admin.site.register(SiteUser, UserAdmin)
