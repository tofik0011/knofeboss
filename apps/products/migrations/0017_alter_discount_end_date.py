# Generated by Django 3.2.9 on 2022-01-29 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_discount_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 30, 16, 35, 21, 292439), verbose_name='admin__end_date'),
        ),
    ]