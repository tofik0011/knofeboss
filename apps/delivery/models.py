from django.db import models
from django.utils.translation import ugettext_lazy as _


# Область;
# Район;
# Населений пункт;
# індекс НП;
# Назва вулиці;
# № будинку;
# Особливості функціонування ВПЗ

# class Region(models.Model):
#     name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
#
#     def __str__(self):
#         return str(self.name)
#
#
# class Settlement(models.Model):
#     id_in_file = models.CharField(unique=False, max_length=255)
#     name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
#     region_fk = models.ForeignKey(Region, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.name)
