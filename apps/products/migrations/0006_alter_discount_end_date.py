# Generated by Django 3.2.9 on 2021-12-01 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_discount_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 2, 16, 22, 14, 589694), verbose_name='admin__end_date'),
        ),
    ]
