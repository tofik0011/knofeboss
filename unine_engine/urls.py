from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.views.static import serve
from filebrowser.sites import site

from mainapp import context_processors

urlpatterns = [
                  path('admin/filebrowser/', site.urls),
                  # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                  path('engine/', admin.site.urls),
                  path('chaining/', include('smart_selects.urls')),
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('lang/', context_processors.lang, name="lang"),
                  path('', include('social_django.urls', namespace='social')),
                  path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
                       name='logout'),

                  re_path(r'^static/(?P<path>.*)$', serve,
                          {'document_root': settings.STATIC_ROOT}),
                  re_path(r'^media/(?P<path>.*)$', serve,
                          {'document_root': settings.MEDIA_ROOT}),
                  path('favicon.ico', RedirectView.as_view(url='/media/icons/favicon.ico'), name='favicon'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("apps.profile.urls")),
    path("", include("mainapp.urls")),
    path("", include("apps.products.urls")),
    path("", include("apps.blog.urls")),
    path("", include("apps.checkout.urls")),
    path("", include("apps.feedback_form.urls")),
    path("", include("apps.testimonials.urls")),
    path("", include("apps.currency.urls")),
    path("", include("apps.nova_poshta.urls")),
    # path("crm/", include("apps.crm.urls")),
    path('', include('social_django.urls', namespace='social')),
    path("", include("apps.products_comparison.urls")),
    # path("", include("modules.notify_when_available.urls")),
    # path("", include("apps.sms.urls")),
    # path("", include("apps.urls")),
    # path("", include("apps.addresses.urls")),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path("", include("apps.custom_page.urls")),  # Завжди має бути в кінці
    prefix_default_language=False,
)
