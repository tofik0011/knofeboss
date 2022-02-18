from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from apps.contacts.models import Email
from apps.email_notifications.views import send_html_mail
from apps.feedback_form.models import FormRequest
from mainapp.helper import validate_email


@csrf_exempt
def add_request(request):
    try:
        name = request.POST.get('name', None)
        country = request.POST.get('country', None)
        cooperation = request.POST.get('cooperation', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        comment = request.POST.get('comment', '')
        error = []

        if len(name) < 1 or name is None:
            error.append({'#ff_name': _('empty_field')})
        if len(country) < 1 or country is None:
            error.append({'#ff_country': _('empty_field')})
        if len(cooperation) < 1 or cooperation is None:
            error.append({'#ff_cooperation': _('empty_field')})
        if len(phone) < 1 or phone is None:
            error.append({'#ff_phone': _('invalid_phone')})
        if not validate_email(email):
            error.append({'#ff_email': _('invalid_email')})
        if len(error) > 0:
            return JsonResponse({'success': False, 'error': error}, safe=False)
        keywords = {}
        if name:
            keywords.update({"name": name})
        if country:
            keywords.update({"country": country})
        if cooperation:
            keywords.update({"cooperation_type": cooperation})
        if phone:
            keywords.update({"phone": phone})
        if email:
            keywords.update({"email": email})
        if country:
            keywords.update({"comment": comment})
        form = FormRequest.objects.create(**keywords)
        try:
            for admin_mail in Email.objects.filter(keyword='feedback_form'):
                send_html_mail('Форма обратной связи', form.get_mail_message(), [admin_mail.email])
        except Exception as e:
            print(str(e))

        return JsonResponse({'success': True, 'message': _('feedback_form__success')}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': _('unknown_error')}, safe=False)
