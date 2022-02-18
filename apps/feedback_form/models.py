from django.db import models
from django.utils.translation import gettext_lazy as _

class FormRequest(models.Model):
    name = models.CharField(verbose_name=_("admin__name_form_form_request"), max_length=255, blank=True)
    country = models.CharField(verbose_name=_("admin__country"), max_length=255, blank=True)
    cooperation_type = models.CharField(verbose_name=_("admin__cooperation_type"), max_length=255, blank=True)
    phone = models.CharField(verbose_name=_("admin__phone"), max_length=255, blank=True)
    email = models.CharField(verbose_name=_("admin__email"), max_length=255, blank=True)
    comment = models.TextField(verbose_name=_("admin__comment"), blank=True)
    date = models.DateTimeField(verbose_name=_("admin__date"), auto_now_add=True)

    class Meta:
        verbose_name = _("admin__form_request")
        verbose_name_plural = _("admin__forms_request")

    def __str__(self):
        try:
            return f'{str(self.date)}, {self.name}'
        except Exception as e:
            return str(self.id)

    def get_mail_message(self):
        return f"""<p>ПІП: <b>{self.name}</b></p>
               <p>Місто: <b>{self.country}</b></p>
               <p>Вид співпраці: <b>{self.cooperation_type}</b></p>
               <p>Телефон: <b>{self.phone}</b></p>
               <p>Email: <b>{self.email}</b></p>
               <p>Коментаррь: <b>{self.comment}</b></p>
               <p>Дата: <b>{self.date.strftime('%d/%m/%Y %H:%M')}</b></p>
           """