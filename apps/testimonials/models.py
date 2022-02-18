from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField


class Testimonial(models.Model):
    author = models.CharField(verbose_name=_('admin__author'), max_length=100, default="", blank=True)
    photo = FileBrowseField(verbose_name=_('admin__image'), max_length=255, directory="testimonials/", extensions=[".jpg", ".png", ".webp"], default="testimonials/unknown_user.jpg", blank=True)
    text = models.TextField(verbose_name=_('admin__testimonial'), default="", blank=True)
    active = models.BooleanField(verbose_name=_('admin__active'), default=False, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    rating = models.IntegerField(verbose_name=_('admin__rating'), blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
