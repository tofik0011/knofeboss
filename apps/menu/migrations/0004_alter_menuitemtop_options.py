# Generated by Django 3.2.9 on 2021-12-01 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20211201_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitemtop',
            options={'verbose_name': 'admin__menu_item_top', 'verbose_name_plural': 'admin__menu_items_top'},
        ),
    ]