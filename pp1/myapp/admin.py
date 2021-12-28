from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import UserProfile
from django.contrib.auth.models import User

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User_Profile'

class CustomAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,CustomAdmin)