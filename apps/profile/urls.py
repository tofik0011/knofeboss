from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token

from apps.profile.api import del_from_wishlist, add_to_wishlist, wishlist_load_more, password_reset, \
    account_password_reset_url, HelloView\
    # , att, TokenView2
from .views import view__account, view__wishlist, view__order_history, view__password_reset, Registration, \
    Authentication, EditProfile, PasswordReset, PasswordResetDone, PasswordResetConfirm, \
    PasswordResetComplete, PasswordChange, AuthMobile, register_by_access_token

urlpatterns = [
    path('login/', Authentication.as_view(), name="view__login"),
    path('auth_mobile/', AuthMobile.as_view(), name="view__auth_mobile"),
    path('registration/', Registration.as_view(), name="view__registration"),
    path('account/', view__account, name="view__account"),
    path('wishlist/', view__wishlist, name="view__wishlist"),
    path('wishlist_load_more/', wishlist_load_more, name="wishlist_load_more"),
    path('order_history/', view__order_history, name="view__order_history"),
    re_path('order_history/(?P<order_id>.+)/$', view__order_history, name="view__single_order"),
    path('edit_profile/', EditProfile.as_view(), name="view__edit_profile"),
    path('password_reset/', view__password_reset, name='view__password_reset'),
    path('api/logout/', LogoutView.as_view(), name="logout"),
    path('api/add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('api/del_from_wishlist/', del_from_wishlist, name='del_from_wishlist'),
    path('api/password_reset/', password_reset, name='account_password_reset'),
    re_path(r'^account_password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', account_password_reset_url,
            name='account_password_reset_url'),

    re_path(r'^password-reset/$', PasswordReset.as_view(), name='password_reset'),
    re_path(r'^password-reset/done/$', PasswordResetDone.as_view(), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PasswordResetConfirm.as_view(),
            name='password_reset_confirm'),
    re_path(r'^password-reset/complete/$', PasswordResetComplete.as_view(), name='password_reset_complete'),
    re_path(r'^password-change/$', PasswordChange.as_view(), name='password_change'),

    re_path(r'^register-by-token/(?P<backend>[^/]+)/$', register_by_access_token, name='register_by_access_token'),
    # re_path(r'^complete_auth/$', CompliteAuth.as_view(), name='complete_auth'),

    path('hello/', HelloView.as_view(), name='hello'),
    # path('att/', att, name='att'),
    # path('att2/', TokenView2.as_view(), name='att2'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
