# Generated by Django 3.2.9 on 2021-11-30 09:38

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import filebrowser.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkout', '0001_initial'),
        ('products', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='admin_profile_type')),
                ('percent_discount', models.IntegerField(blank=True, default=0, null=True, verbose_name='admin__percent_discount')),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='admin__min_price')),
                ('default', models.BooleanField(default=False, verbose_name='admin__default')),
                ('keyword', models.CharField(max_length=255, verbose_name='admin_type_keyword')),
            ],
            options={
                'verbose_name': 'admin_type_profile',
                'verbose_name_plural': 'admin_type_profiles',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, default='', max_length=255, verbose_name='admin_phone')),
                ('picture', filebrowser.fields.FileBrowseField(blank=True, max_length=255, verbose_name='admin__image')),
                ('cart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkout.cart', verbose_name='admin__cart')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('type_profile_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile.typeprofile')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('wishlist', models.ManyToManyField(blank=True, to='products.Product', verbose_name='admin_wishlist')),
            ],
            options={
                'verbose_name': 'admin_profile',
                'verbose_name_plural': 'admin_profiles',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
