from django.db import models
from django.utils.translation import ugettext_lazy as _


# Область;
# Район;
# Населений пункт;
# індекс НП;
# Назва вулиці;
# № будинку;
# Особливості функціонування ВПЗ

class Settlement(models.Model):
    ref = models.CharField(max_length=255,blank=True)
    settlement_type = models.CharField(max_length=255,blank=True)
    description = models.CharField(max_length=255,blank=True)
    area = models.CharField(max_length=255,blank=True)
    area_description = models.CharField(max_length=255,blank=True)
    region = models.CharField(max_length=255,blank=True)
    region_description = models.CharField(max_length=255,blank=True)
