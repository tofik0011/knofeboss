from django.http import HttpResponseRedirect
from .models import Redirects


class RedirectsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("kek")
        response = self.get_response(request)
        if 'text/html' in response.get('Content-Type', ''):
            redirect_item = Redirects.objects.filter(redirect_from=request.build_absolute_uri()).values('redirect_to', 'status_code').first()

            if redirect_item:
                resp = HttpResponseRedirect(redirect_item['redirect_to'])
                resp.status_code = redirect_item['status_code']
                return resp
        return response
