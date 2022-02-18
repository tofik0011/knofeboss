from django.urls import path
from . import views

urlpatterns = [
    path("api/newsletter_add/", views.newsletterAdd, name="add_newsletter"),
]
