# Generated by Django 3.2.9 on 2021-12-01 13:47

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='menu_keyword',
        ),
        migrations.CreateModel(
            name='MenuItemTOP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='admin__order')),
                ('active', models.BooleanField(default=True, verbose_name='admin__active')),
                ('link', models.CharField(blank=True, default='', help_text="Пример: '/ru/catalog/'. Указывать со / вначале и в конце. Код языка также указывается (кроме ссылок на основном языке сайта).", max_length=255, verbose_name='admin__link')),
                ('title', models.CharField(blank=True, default='', max_length=255, verbose_name='admin__title')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.menuitemtop', verbose_name='admin__parent_menu')),
            ],
            options={
                'verbose_name': 'admin__menu_item',
                'verbose_name_plural': 'admin__menu_items',
            },
        ),
    ]
