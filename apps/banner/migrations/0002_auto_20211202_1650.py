# Generated by Django 3.2.9 on 2021-12-02 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='button_text',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='button_text_ru',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='button_text_uk',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='content_color',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='content_position',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='overlay_color',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='overlay_opacity',
        ),
    ]