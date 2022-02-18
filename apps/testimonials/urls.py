from django.urls import path
from . import views

urlpatterns = [
    path("testimonials/", views.view__testimonials, name="view__testimonials"),
    path("api/add_testimonial/", views.add_testimonial, name="add_testimonial"),
    path("api/view__testimonials_model/", views.view__testimonials_model, name="view__testimonials_model")
]
