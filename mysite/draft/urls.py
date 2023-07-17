from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'draft'

urlpatterns = [
    path('create', views.draft_create, name='createdraft'),
]