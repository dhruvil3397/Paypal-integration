from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Blogpost

# Register your models here.
class BlogpostAdmin(ModelAdmin):
    list_display = ['title','heading1','heading2','heading3']

admin.site.register(Blogpost,BlogpostAdmin)
