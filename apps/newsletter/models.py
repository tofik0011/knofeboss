from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from ckeditor.fields import RichTextField


class NewsletterUser(models.Model):
    mail = models.CharField(_("email"), max_length=255, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletters")


class NewsletterMailing(models.Model):
    subject = models.CharField(verbose_name=_("admin_subject"), max_length=255, default="subject", blank=True)
    content = RichTextField(verbose_name=_("admin_content"), default=None, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("admin__mailing")
        verbose_name_plural = _("admin__mailing")

    def save(self, *args, **kwargs):
        users = NewsletterUser.objects.values_list('email', flat=True).all()
        send_mail(self.subject, self.content, "KOLO", users, fail_silently=False)
        super(NewsletterMailing, self).save(*args, **kwargs)
