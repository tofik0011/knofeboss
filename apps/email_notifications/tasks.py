from time import sleep
from django.core.mail import send_mail

from apps.contacts.models import Phone
from unine_engine.celery import app


@app.task
def my_task():
    # i = Phone.objects.create(phone='123123', keyword='wqe', order=1)
    sleep(5)
    print('Хуййййй')
    return {'success': True}
    # send_mail('kek', 'message', 'eleven.te.ua@gmail.com', ['eleven.te.ua@gmail.com'], fail_silently=False)
