from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group
from django.forms import TextInput
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse, path, re_path
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from apps.nova_poshta import models
from apps.profile.models import Profile, Group, GroupProxy, TypeProfile
from django.apps import apps


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False

@admin.register(TypeProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TypeProfile._meta.fields]


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    # save_as = True
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'picture', 'phone', 'type_profile_fk')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # list_display = ('date_joined', 'account_actions', 'is_apporved', 'last_name', 'first_name', 'account_phone', 'email', 'is_staff')
    # list_editable = ('is_staff',)
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    #     (_('Permissions'), {
    #         'fields': ('is_active', 'is_staff'),
    #     }),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # inlines = (ProfileInline,)
    ordering = ("-date_joined",)

    # def approve_account(self, obj):
    #     return render_to_string('account/approved.html', {'test': 'test1'})
    #
    # approve_account.short_description = 'Подтверждение пользователя'


# Перерегистрируем модель User
admin.site.unregister(Group)
admin.site.register(GroupProxy)
