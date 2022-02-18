from django.shortcuts import render
from django.utils.translation import get_language
from rest_framework.generics import get_object_or_404

from mainapp.get_data import validate_email
from .models import NewsletterUser
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext_lazy as _


def newsletterAdd(request):
    email = request.POST.get('mail', None)
    if not validate_email(email):
        return JsonResponse({"success": False, "message": _("invalid_email")})
    try:
        if NewsletterUser.objects.filter(mail=email):
            return JsonResponse({"success": False, "message": _("newsletter_alredy_exists")})
        NewsletterUser.objects.create(mail=email)
        return JsonResponse({"success": True, "message": _('newsletter_success')})
    except Exception as ex:
        print(str(ex))
        return JsonResponse({"success": False, "message": _('unknown_error')})
