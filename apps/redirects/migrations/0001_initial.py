# Generated by Django 3.2.9 on 2021-11-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Redirects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_from', models.CharField(max_length=255)),
                ('redirect_to', models.CharField(max_length=255)),
                ('status_code', models.IntegerField(default=301)),
            ],
        ),
    ]
