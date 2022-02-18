# Generated by Django 3.2.9 on 2022-01-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0007_alter_banner_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='keyword',
            field=models.CharField(choices=[('mainpage', 'admin__mainpage'), ('mainpage_second', 'admin__mainpage_second'), ('mainpage_third', 'admin__mainpage_third')], max_length=255, unique=True, verbose_name='admin__keyword'),
        ),
    ]
