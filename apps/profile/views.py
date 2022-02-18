from time import sleep
from urllib.error import HTTPError

# from oauth2_provider.oauth2_validators import OAuth2Validator
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView
from django.http import JsonResponse, response, HttpResponsePermanentRedirect, HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from social_core.actions import do_auth
from social_core.backends.utils import get_backend
from social_core.exceptions import MissingBackend
from social_django.models import UserSocialAuth
from social_django.views import NAMESPACE, _do_login

from apps.profile.forms import RegistrationForm, AuthenticationForm, EditAccountForm, DivErrorList
from apps.profile.models import Profile, TypeProfile
from apps.checkout.models import Order
from django.utils.translation import gettext_lazy as _

from mainapp.helper import print_c
from unine_engine.globals import USER_TYPES
from social_django.utils import load_backend, BACKENDS, psa, load_strategy


class PasswordReset(PasswordResetView):
    template_name = "account/password_reset.html"
    # html_email_template_name = "account/password_reset.html"
    # email_template_name = "account/password_reset.html"


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    title = _('Password_reset_sent')


class PasswordResetConfirm(PasswordResetConfirmView):
    PasswordResetConfirmView.form_class.error_messages = {
        'password_mismatch': _('The_two_password_fields_didn’t_match.'),
    }
    template_name = 'account/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    PasswordResetCompleteView.title = _('Password_reset_complete')
    template_name = 'account/password_reset_complete.html'


class PasswordChange(PasswordChangeView):
    template_name = 'account/password_change_form.html'


@psa('social:complete')
def register_by_access_token(request, backend):
    try:
        token = request.GET.get('access_token')
        user = request.backend.do_auth(token)
        if user:
            login(request, user)
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})
    except Exception as ex:
        return JsonResponse({"status": False, 'error': str(ex)})


# class CompliteAuth(View, OAuth2Validator):
#     def get(self, request):
#         request.session['redirect_after_login_url'] = 1
#         if 'redirect_after_login_url' in request.session:
#             # del request.session['redirect_after_login_url']  ВЕРНУТИ ОБОВЯЗКОВО
#             HttpResponseRedirect.allowed_schemes += ['xamarinessentials']
#             user_s = UserSocialAuth.objects.get(user_id=request.user.id, provider=request.session['social_auth_last_login_backend'])
#             token, _ = Token.objects.get_or_create(user=user_s.user)
#             # from oauthlib.oauth2.rfc6749.tokens import BearerToken
#             # barrer = BearerToken()
#             # request.scopes = ['read', 'write']
#             #
#             # request.extra_credentials = None
#             # token = barrer.create_token(request, False)
#             # print("")
#             return HttpResponseRedirect(f'xamarinessentials://#access_token={user_s.extra_data["access_token"]}&expires={user_s.extra_data["expires"]}&token={token.key}')
#         else:
#             return redirect('/')


class AuthMobile(View):
    def get(self, request):
        social = request.GET.get("social")
        request.session['redirect_after_login_url'] = 1
        # http://127.0.0.1:8000/auth_mobile/?social=google-oauth2
        # http://127.0.0.1:8000/login/google-oauth2/
        return redirect(f"/login/{social}/")
        # return response.HttpResponseRedirect("igreenmobile://#access_token=12345&refresh_token=12345&expires=34354345345")
        # return redirect("https://www.google.com/",)


class Registration(View):
    def get(self, request):
        type_profile = TypeProfile.objects.all()
        return render(request, 'account/registration.html', context={'account_types': type_profile})

    def post(self, request):
        form_data = request.POST
        errors = Profile.registration_form_validate(form_data, request)
        if len(errors) > 0:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            Profile.create_user(form_data)
            return JsonResponse({'success': True, 'message': _('account__registration_success')})


class Authentication(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('view__account'))
        return render(request, 'account/login.html', context={'account_types': USER_TYPES})

    def post(self, request):
        form_data = request.POST
        res = Profile.authentication_form_validate(form_data, request)
        if res['success'] is False:
            return JsonResponse(res)
        else:
            login(request, res['user'])
            return JsonResponse({'success': True, 'redirect': reverse('view__account')})


class EditProfile(View):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if not request.user.is_authenticated:
            return redirect(reverse('view__login'))
        type_profile = TypeProfile.objects.all()
        return render(request, 'account/parts/edit_profile.html', context={'account_types': type_profile, 'active': 'edit_profile'})

    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        res = user.edit_profile_data(request.POST, request)
        print(res)
        if res['success'] is False:
            return JsonResponse(res)
        else:
            return JsonResponse({'success': True})


@login_required
def view__account(request):
    return redirect(reverse('view__order_history'))


def view__password_reset(request):
    return render(request, 'account/password_reset.html')


@login_required
def view__wishlist(request):
    return render(request, 'account/parts/wishlist.html', {'active': 'wishlist'})


@login_required
def view__order_history(request, order_id=None):
    """Если нету order_id отдает весь список заказов
    Если order_id присутствует отдает детальную информацию об этом заказе
    """
    page = request.GET.get('page', 1)
    user = request.user
    if order_id:
        order = Order.objects.get(id=order_id)
        if order.user.id != user.id:
            return redirect(reverse('view__login'))
        else:
            return render(request, 'account/parts/order_detail.html', {'order': order})
    return render(request, 'account/parts/order_history.html', {'active': 'order_history', 'orders': user.get_orders_list(page=page, limit=2)})
