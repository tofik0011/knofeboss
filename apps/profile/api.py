import re
import secrets
import string
from datetime import timedelta

import requests
from django.contrib.auth import authenticate, login, logout as logout_f, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
# from oauth2_provider.models import AccessToken
# from oauth2_provider.oauth2_validators import Application
# from oauth2_provider.views import TokenView
from oauthlib.oauth2 import RequestValidator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profile.models import Profile
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.email_notifications.views import send_html_mail
from mainapp.helper import validate_email
from unine_engine import settings, globals


@csrf_exempt
def wishlist_load_more(request):
    wishlist, hes_next_page = request.user.get_wishlist(page=request.POST.get('page', 1))
    return JsonResponse(
        {'template': render_to_string('account/parts/wishlist_items.html', {'wishlist': wishlist}, request),
         'has_next_page': hes_next_page})


@csrf_exempt
def del_from_wishlist(request):
    product_id = request.POST.get('product_id', None)
    try:
        res = {'success': request.user.del_product_from_wishlist(product_id)}
    except Exception as ex:
        res = {'success': False, 'redirect': reverse('view__login')}
    return JsonResponse(res)


@csrf_exempt
def add_to_wishlist(request):
    product_id = request.POST.get('product_id', None)
    try:
        notification_data = {'heading': _('account__added_to_wishlist'),
                             'buttons': [{'link': reverse('view__wishlist'), 'text': _('go_to')}]}
        notification = None  # render_to_string('mainapp/parts/notification.html', notification_data)
        res = {'success': request.user.add_product_to_wishlist(product_id), 'notification': notification}
    except Exception as ex:
        res = {'success': False, 'redirect': reverse('view__login')}
    return JsonResponse(res)


def password_reset(request):
    email = request.POST.get('email', None)
    if validate_email(email):
        user = User.objects.filter(email=email).first()
        if user:
            url = 'https://' if request.is_secure() else 'http://'
            url += request.get_host() + reverse('account_password_reset_url',
                                                kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                                                        'token': default_token_generator.make_token(user)})
            body = 'Ссылка для востановления пароля: <a href="' + url + '">' + url + '</a>\n Перейдите поссылке чтобы получить новый пароль.'
            send_html_mail('Tatoshka: Password Reset', body, email)
            return JsonResponse({'success': True, 'message': _('account_password_reset_success_message')})
        else:
            return JsonResponse({'success': False, 'message': _('account__password_reset_email_doesnt_exist')})
    else:
        return JsonResponse({'success': False, 'message': _('account__incorrect_email')})



def account_password_reset_url(request, *args, **kwargs):
    uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
    user = Profile.objects.get(pk=uid)
    token = kwargs['token']
    if default_token_generator.check_token(user, token):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        user.set_password(password)
        user.save()
        send_html_mail('Tatoshka: Password Reset', 'New password: ' + password, user.email)
        print('new password', password)
        return render(request, 'account/password_reset_accepting_done.html', {})
    else:
        print('bad token')
    return render(request, 'account/password_reset_accepting_done.html', {'error': _('bad_token_try_again')})


# def att(request):
#     headers = {'Authorization': 'Bearer wW7qoryvtxhujVsRQzRkjUvMP11iQO'}
#
#     response_uri = f'https://example.com/callback#access_token=wW7qoryvtxhujVsRQzRkjUvMP11iQO&state={"ss345asyht"}&token_type=Bearer&scope=read+write'
#
#     from oauthlib.oauth2 import MobileApplicationClient, LegacyApplicationClient
#     from oauthlib.common import Request
#
#     # rr = requests.post("http://127.0.0.1:8000/o/token/", data={
#     #     'grant_type': 'password',
#     #     'client_id': '5lE9LPGcEP17BFUwgciKR8NpfW89vEp2Rgd4inyG',
#     #     'client_secret': 'PXHIubfkXqEC4dEYPcEU0JKVXz2gu4F6mhxMzFmLaCCjGLd1VIc928xr90qFGtQfopSkfaoOjeoZYZcK4vQHmgQFkpOBM5ZW6SCpPwDHMvqvgQ62DsDF1jtZqfoEdqur',
#     #     'username': 'admin',
#     #     'password': 'admin',
#     # })
#     # from oauthlib.oauth2 import LegacyApplicationClient
#     # from requests_oauthlib import OAuth2Session
#     # oauth = OAuth2Session(client=LegacyApplicationClient(client_id='5lE9LPGcEP17BFUwgciKR8NpfW89vEp2Rgd4inyG'))
#     # token = oauth.fetch_token(token_url='http://127.0.0.1:8000/o/token/',verify=False,
#     #                                username="admin", password="admin", client_id="PXHIubfkXqEC4dEYPcEU0JKVXz2gu4F6mhxMzFmLaCCjGLd1VIc928xr90qFGtQfopSkfaoOjeoZYZcK4vQHmgQFkpOBM5ZW6SCpPwDHMvqvgQ62DsDF1jtZqfoEdqur",
#     #                                client_secret='client_secret')
#
#     user = Profile.objects.filter(id=request.user.id).first()
#     if user:
#         app = Application.objects.get(client_id="5lE9LPGcEP17BFUwgciKR8NpfW89vEp2Rgd4inyG")
#         AccessToken.objects.get_or_create(user=user,
#                                           application=app,
#                                           expires=now() + timedelta(days=365),
#                                           token="qwerewt934532jtnnqwj2u2")
#     validator = RequestValidator()
#     request.headers = headers
#     rere = Request(response_uri, headers=headers)
#     validator.authenticate_client_id('5lE9LPGcEP17BFUwgciKR8NpfW89vEp2Rgd4inyG', rere)
#     return JsonResponse({})


# @method_decorator(csrf_exempt, name="dispatch")
# class TokenView2(TokenView):
#     @method_decorator(sensitive_post_parameters("password"))
#     def post(self, request, *args, **kwargs):
#         sup_resp = super(TokenView2, self).post(request, *args, **kwargs)
#         print('kek')
#         return sup_resp


class HelloView(APIView):
    # permission_classes = (AllowAny,)
    # @permission_classes([AllowAny])

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
