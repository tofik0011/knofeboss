# Generated by Django 3.2.9 on 2021-12-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20211201_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitemtop',
            name='link_ru',
            field=models.CharField(blank=True, default='', help_text="Пример: '/ru/catalog/'. Указывать со / вначале и в конце. Код языка также указывается (кроме ссылок на основном языке сайта).", max_length=255, null=True, verbose_name='admin__link'),
        ),
        migrations.AddField(
            model_name='menuitemtop',
            name='link_uk',
            field=models.CharField(blank=True, default='', help_text="Пример: '/ru/catalog/'. Указывать со / вначале и в конце. Код языка также указывается (кроме ссылок на основном языке сайта).", max_length=255, null=True, verbose_name='admin__link'),
        ),
        migrations.AddField(
            model_name='menuitemtop',
            name='title_ru',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='admin__title'),
        ),
        migrations.AddField(
            model_name='menuitemtop',
            name='title_uk',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='admin__title'),
        ),
    ]