from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('home/', views.home,name="Bloghome"),
    path('blogpost/<int:id>', views.blogpost,name="Blogpost"),
]