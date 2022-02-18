from django import http
from django.urls import translate_url
from django.conf import settings
from django.utils.http import is_safe_url
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language
)
from django.http import HttpResponse

DEFAULT_PACKAGES = ['django.conf']
LANGUAGE_QUERY_PARAMETER = 'language'

# TODO на соплі полюбому шось можна краще написать
def lang(request):
    next = str(request.POST.get('next'))
    for lan in dict(settings.LANGUAGES):
        next = next.replace('/' + lan, '')
    # next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, allowed_hosts=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            next_trans = translate_url(next, lang_code)

            if next_trans != next:
                response = http.HttpResponseRedirect(next_trans)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                    max_age=settings.LANGUAGE_COOKIE_AGE,
                                    path=settings.LANGUAGE_COOKIE_PATH,
                                    domain=settings.LANGUAGE_COOKIE_DOMAIN)

    return HttpResponse(response.url)
