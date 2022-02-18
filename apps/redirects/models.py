from django.db import models


class Redirects(models.Model):
    redirect_from = models.CharField(max_length=255, null=False)
    redirect_to = models.CharField(max_length=255, null=False)
    status_code = models.IntegerField(default=301, null=False)
