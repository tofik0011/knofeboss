# Generated by Django 3.2.9 on 2021-11-30 09:38

import django.core.validators
from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, default='', max_length=100, verbose_name='admin__author')),
                ('photo', filebrowser.fields.FileBrowseField(blank=True, default='testimonials/unknown_user.jpg', max_length=255, verbose_name='admin__image')),
                ('text', models.TextField(blank=True, default='', verbose_name='admin__testimonial')),
                ('active', models.BooleanField(blank=True, default=False, verbose_name='admin__active')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='admin__rating')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
    ]
