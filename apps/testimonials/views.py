import errno
import os

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from filebrowser.base import FileObject
from unine_engine import globals
from apps.testimonials.models import Testimonial
from django.utils.translation import ugettext_lazy as _


def save_file(file_byte, name):
    if not os.path.exists(os.path.dirname(name)):
        try:
            os.makedirs(os.path.dirname(name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    try:
        with open(name, "wb") as file:
            file.write(file_byte)
    except Exception as ex:
        print(ex)


def view__testimonials(request):
    page = request.GET.get('page', 1)
    testimonials = Testimonial.objects.filter(active=True).all()
    testimonials = Paginator(testimonials, 6).page(page)
    return render(request, "testimonials/testimonials_page.html", {'testimonials': testimonials})


@csrf_exempt
def view__testimonials_model(request):
    return render(request, "testimonials/modal.html")


@csrf_exempt
def add_testimonial(request):
    _photo = ""
    author = request.POST.get('author', None)
    text = request.POST.get('text', None)
    rating = request.POST.get('rating', None)
    try:
        _photo = f'{globals.MEDIA_ROOT}/testimonials/{request.FILES["photo"].name}'
        save_file(request.FILES['photo'].read(), _photo)
        _photo = FileObject(f'testimonials/{request.FILES["photo"].name}')
    except Exception as ex:
        pass
    if not author or not text:
        return JsonResponse({"success": False, "message": _('fill_in_fields')})
    try:
        if _photo == "":
            testimonials = Testimonial.objects.create(author=author, text=text, rating=rating, active=False)
        else:
            testimonials = Testimonial.objects.create(author=author, text=text, photo=_photo, rating=rating, active=False)
        return JsonResponse({"success": True, "message": _('testimonials__success_message')})
    except Exception as ex:
        print(ex)
        return JsonResponse({"success": False, "message": _('unknown_error')})
