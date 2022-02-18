from datetime import datetime
import re
from django.contrib.auth.models import User
from django.db import models
from filebrowser.fields import FileBrowseField
from unine_engine.globals import LANGUAGES, USER_TYPES
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.timezone import make_aware


class Procedure(models.Model):
    price = models.PositiveIntegerField(_('name'), blank=True)
    duration = models.PositiveIntegerField(_('duration'), blank=True, default=0)

    def __str__(self):
        try:
            return self.procedurelanguage_set.filter(language=get_language()).first().name
        except Exception as e:
            return self.id


class ProcedureLanguage(models.Model):
    language = models.CharField(_('lang'), max_length=15, choices=LANGUAGES)
    procedure_fk = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=255, blank=True)

    def __str__(self):
        return self.name


class ExtendedUser(User):
    phone = models.CharField("Telephone", max_length=20, default="")
    date_of_birth = models.DateField(verbose_name=_('account__date_of_birth'), auto_now_add=False, auto_now=False, null=True)
    avatar = FileBrowseField("Image", max_length=200, directory="account/", extensions=[".jpg", ".webp", ".png"], blank=True, null=True)
    type = models.CharField(choices=USER_TYPES, default='client', max_length=64)


class Master(models.Model):
    user_fk = models.OneToOneField(ExtendedUser, on_delete=models.CASCADE)
    procedures_list = models.ManyToManyField(Procedure, verbose_name=_('account__wishlist'), blank=True)

    def get_day_schedule(self, date):
        date = make_aware(date)
        appointments = Appointment.objects.filter(master_fk_id=self.id, start__day=date.day, start__year=date.year, start__month=date.month).order_by('start')
        res = []
        print(len(appointments))
        for a in appointments:
            print(a)
            res.append({
                'start': a.start.strftime('%H:%M'),
                'end': a.end.strftime('%H:%M'),
                'duration': a.procedure_fk.duration,
            })
        return res


def __str__(self):
    return self.user_fk.first_name


class Client(models.Model):
    user_fk = models.OneToOneField(ExtendedUser, on_delete=models.CASCADE)


class Appointment(models.Model):
    client_fk = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    procedure_fk = models.ForeignKey(Procedure, on_delete=models.SET_NULL, null=True)
    master_fk = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField(auto_now=False, default=datetime.now)
    end = models.DateTimeField(auto_now=False, default=datetime.now)

    def __str__(self):
        try:
            return f'{datetime.strftime(self.start,"%d.%m.%Y")} - {datetime.strftime(self.end,"%d.%m.%Y")}, Client:{self.client_fk.user_fk.first_name}, Master:{self.master_fk.user_fk.first_name}'
        except Exception as e:
            return self.id
