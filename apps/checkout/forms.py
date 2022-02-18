from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.utils.translation import gettext, gettext_lazy as _
from mainapp.helper import validate_email, validate_phone
from unine_engine import globals as GLOBALS


class CheckoutForm(forms.Form):
    # required_css_class = 'rrr'
    # error_css_class = 'error'

    first_name = forms.CharField(label=_('account__first_name'), max_length=255)
    last_name = forms.CharField(label=_('account__last_name'), max_length=255)
    email = forms.CharField(label=_('email'), min_length=2, max_length=255)
    phone = forms.CharField(label=_('phone'), min_length=2, max_length=255)
    delivery_type = forms.ChoiceField(label=_('checkout__delivery_type'), required=True, widget=forms.Select, choices=GLOBALS.DELIVERY_CHOICES, initial=_('select'))
    payment_type = forms.ChoiceField(label=_('checkout__payment_type'), required=True, widget=forms.Select, choices=GLOBALS.PAYMENT_CHOICES)
    delivery_settlement = forms.CharField(label=_('checkout__settlement'), min_length=2, max_length=255)
    delivery_address = forms.CharField(label=_('checkout__address'), min_length=2, max_length=255)
    post_index = forms.CharField(label=_('checkout__post_index'), min_length=2, max_length=255)
    privacy_policy = forms.BooleanField(widget=forms.CheckboxInput)
    comment = forms.CharField(widget=forms.Textarea)

    first_name.widget.attrs.update({'class': 'input_v1'})
    last_name.widget.attrs.update({'class': 'input_v1'})
    email.widget.attrs.update({'class': 'input_v1'})
    phone.widget.attrs.update({'class': 'input_v1', 'placeholder': '+380XXXXXXXXX'})
    delivery_type.widget.attrs.update({'class': 'input-field', 'id': 'delivery_type'})
    payment_type.widget.attrs.update({'class': 'select_v1'})
    privacy_policy.widget.attrs.update({'class': 'filled-in'})
    delivery_settlement.widget.attrs.update({'class': 'input_v1', 'id': 'delivery_settlement', 'style': 'display:none'})
    delivery_address.widget.attrs.update({'class': 'input_v1', 'id': 'delivery_address', 'style': 'display:none'})
    post_index.widget.attrs.update({'class': 'input_v1', 'id': 'post_index', 'style': 'display:none'})
    comment.widget.attrs.update({'class': 'input_v1', 'placeholder': _('checkout__comment'), 'rows': 3, 'cols': 30, 'style': 'resize:none'})

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 2:
            raise ValidationError(_('error__first_name_min_length'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 2:
            raise ValidationError(_('error__last_name_min_length'))
        return last_name

    def clean_phone(self):
        new_phone = self.cleaned_data['phone']
        if not validate_phone(new_phone):
            raise ValidationError(_('error__invalid_phone'))
        return new_phone

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if not validate_email(new_email):
            raise ValidationError(_('error__incorrect_email'))
        return new_email

    def clean(self):
        dp = self.cleaned_data['delivery_type']
        show_fields = []
        if dp in ['new_post', 'avtoluks', 'delivery', 'ukr_post', 'in_time']:
            show_fields = ['delivery_settlement', 'delivery_address']
            if self.cleaned_data['delivery_settlement']:
                raise ValidationError({'delivery_settlement': ValidationError(_('error__empty_field'))})
            if self.cleaned_data['delivery_address']:
                raise ValidationError({'delivery_address': ValidationError(_('error__empty_field'))})
        if dp in ['avtoluks', 'delivery', 'ukr_post', 'in_time']:
            show_fields = ['delivery_settlement', 'delivery_address', 'post_index']
        for f in show_fields:
            attrs = self.fields[f].widget.attrs
            attrs.update({'style': 'display:block'})
        # if dp == 'new_post':
        #     address = f'{self.cleaned_data["delivery_settlement"]}, {self.cleaned_data["delivery_address"]}'
        # elif dp != 'pickup':
        #     if not self.cleaned_data['delivery_settlement']:
        #         raise ValidationError({'delivery_settlement': ValidationError(_('empty_field'))})

        #     if not delivery_street:
        #         error.append({'other_delivery_street_input': _('empty_field')})
        # if not payment_type or payment_type == "-1":
        #     error.append({'payment_type': _('select_payment_type')})
        #
        # if not police or police == "false":
        #     error.append({'police_label': _('police_required')})
        #
        # if d['delivery_type'] != 'pickup':
        #     delivery_address =
        #     if d['post_index']:
        #         delivery_address += f' [{d["post_index"]}]'
        # else:
        #     delivery_address = None
