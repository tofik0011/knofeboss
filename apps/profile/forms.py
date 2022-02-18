from django import forms
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.profile.models import Profile
from mainapp.helper import validate_email, validate_phone
from unine_engine import globals as GLOBALS
from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])


class RegistrationForm(forms.Form):
    email = forms.CharField(label=_('email'), label_suffix='', required=False, max_length=255)
    first_name = forms.CharField(label=_('account__first_name'), required=False, label_suffix='', max_length=255)
    last_name = forms.CharField(label=_('account__last_name'), required=False, label_suffix='', max_length=255)
    phone = forms.CharField(label=_('phone'), label_suffix='', required=False, max_length=255)
    type = forms.ChoiceField(label=_('account__client_type'), required=False, label_suffix='', widget=forms.Select, choices=GLOBALS.USER_TYPES, help_text="Client type")
    password = forms.CharField(label=_('account__password'), widget=forms.PasswordInput, required=False, label_suffix='', max_length=255)
    password_confirm = forms.CharField(label=_('account__repeat_password'), widget=forms.PasswordInput, required=False, label_suffix='', max_length=255)

    first_name.widget.attrs.update({'class': 'input_v1'})
    last_name.widget.attrs.update({'class': 'input_v1'})
    email.widget.attrs.update({'class': 'input_v1'})
    phone.widget.attrs.update({'class': 'input_v1 phone_input'})
    type.widget.attrs.update({'class': 'select_v1'})
    password.widget.attrs.update({'class': 'input_v1'})
    password_confirm.widget.attrs.update({'class': 'input_v1'})

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if not new_email:
            raise ValidationError(_('error__required_field'))
        if not validate_email(new_email):
            raise ValidationError(_('error__invalid_email'))
        if User.objects.filter(username__iexact=self.cleaned_data['email']).exists():
            raise ValidationError(_('error__email_is_already_in_use'))
        return new_email

    def clean_first_name(self):
        new_first_name = self.cleaned_data.get('first_name')
        if not new_first_name:
            raise ValidationError(_('error__required_field'))
        return new_first_name

    def clean_last_name(self):
        new_last_name = self.cleaned_data.get('last_name')
        if not new_last_name:
            raise ValidationError(_('error__required_field'))
        return new_last_name

    def clean_phone(self):
        new_phone = self.cleaned_data.get('phone').replace(' ', '')
        if not new_phone:
            raise ValidationError(_('error__required_field'))
        if not validate_phone(new_phone):
            raise ValidationError(_('error__invalid_phone'))
        return new_phone

    def clean_password(self):
        new_password = self.cleaned_data.get('password')
        if not new_password:
            raise ValidationError(_('error__required_field'))
        if len(self.cleaned_data['password']) < 6:
            raise ValidationError(_('error__min_length').format(6))
        return self.cleaned_data['password']

    def clean(self):
        super(RegistrationForm, self).clean()
        print(self.cleaned_data)
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('password_confirm')
        if not re_password:
            raise ValidationError({'password_confirm': ValidationError(_('error__required_field'))})
        if password != re_password:
            raise ValidationError({'password_confirm': ValidationError(_('error__passwords_are_not_equal'))})

    def save(self):
        return Account.create_user(self.cleaned_data)


class AuthenticationForm(forms.Form):
    username = forms.CharField(label=_('email'), label_suffix='', required=False, max_length=255)
    password = forms.CharField(label=_('account__password'), label_suffix='', required=False, max_length=255, widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'input_v1', 'placeholder': _('email')})
    password.widget.attrs.update({'class': 'input_v1', 'placeholder': _('account__password')})

    def clean_username(self):
        _username = self.cleaned_data.get('username', None)
        if not _username:
            raise ValidationError(_('error__enter_email'))
        return _username

    def clean_password(self):
        _password = self.cleaned_data.get('password', None)
        if not _password:
            raise ValidationError(_('error__enter_password'))
        return _password

    def clean(self):
        super(AuthenticationForm, self).clean()
        _username = self.cleaned_data.get('username', None)
        _password = self.cleaned_data.get('password', None)
        user = authenticate(username=_username, password=_password)
        if _username and _password:
            if not user or not user.check_password(_password):
                raise ValidationError({'password': ValidationError(_('error__invalid_credentials'))})


class EditAccountForm(forms.Form):
    username = forms.CharField(label=_('email'), label_suffix='', required=False, max_length=255)
    first_name = forms.CharField(label=_('account__first_name'), required=False, label_suffix='', max_length=255)
    last_name = forms.CharField(label=_('account__last_name'), required=False, label_suffix='', max_length=255)
    phone = forms.CharField(label=_('phone'), label_suffix='', required=False, max_length=255)
    type = forms.ChoiceField(label=_('account__client_type'), required=False, label_suffix='', widget=forms.Select, choices=GLOBALS.USER_TYPES, help_text="Client type")
    current_password = forms.CharField(label=_('account__current_password'), widget=forms.PasswordInput, required=False, label_suffix='', max_length=255)
    new_password = forms.CharField(label=_('account__password'), widget=forms.PasswordInput, required=False, label_suffix='', max_length=255)
    new_password_confirm = forms.CharField(label=_('account__repeat_password'), widget=forms.PasswordInput, required=False, label_suffix='', max_length=255)

    username.widget.attrs.update({'class': 'input_v1','disabled':'disabled'})
    first_name.widget.attrs.update({'class': 'input_v1'})
    last_name.widget.attrs.update({'class': 'input_v1'})
    phone.widget.attrs.update({'class': 'input_v1 phone_input'})
    type.widget.attrs.update({'class': 'select_v1'})
    new_password.widget.attrs.update({'class': 'input_v1'})
    new_password_confirm.widget.attrs.update({'class': 'input_v1'})

    def clean_first_name(self):
        new_first_name = self.cleaned_data.get('first_name')
        if not new_first_name:
            raise ValidationError(_('error__required_field'))
        return new_first_name

    def clean_last_name(self):
        new_last_name = self.cleaned_data.get('last_name')
        if not new_last_name:
            raise ValidationError(_('error__required_field'))
        return new_last_name

    def clean_phone(self):
        new_phone = self.cleaned_data.get('phone').replace(' ', '')
        if not new_phone:
            raise ValidationError(_('error__required_field'))
        if not validate_phone(new_phone):
            raise ValidationError(_('error__invalid_phone'))
        return new_phone

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = authenticate(username=self.cleaned_data['username'], password=current_password)
        if not current_password:
            raise ValidationError(_('error__required_field'))
        if not user or not user.check_password(current_password):
            raise ValidationError(_('error__invalid_credentials'))
        return current_password

    def clean(self):
        super(EditAccountForm, self).clean()
        np = self.cleaned_data.get('new_password', None)
        npc = self.cleaned_data.get('new_password_confirm', None)
        if np or npc:
            if len(np) < 6:
                raise ValidationError({'new_password': ValidationError(_('error__min_length').format(6))})
            if np != npc:
                raise ValidationError({'new_password_confirm': ValidationError(_('error__passwords_are_not_equal'))})

    def save(self, **kwargs):
        request = kwargs.pop('request')
        user = authenticate(username=request.user.username, password=self.cleaned_data['current_password'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.account.phone = self.cleaned_data['phone']

        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
            update_session_auth_hash(request, user)
