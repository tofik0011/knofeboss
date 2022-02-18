from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from django.urls import path, include

urlpatterns = [
    path('api/feedback_form_add/', add_request, name="feedback_form__add_message"),
]
