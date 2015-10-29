# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150928_1109'),
        ('cmsplugin_profile', '0003_auto_20151026_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='detail_image',
            field=filer.fields.image.FilerImageField(related_name='profile_detail', on_delete=django.db.models.deletion.SET_NULL, default=None, to='filer.Image', blank=True, help_text='Image must be 1:1 aspect ratio', null=True, verbose_name='Detail Image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='thumbnail_image',
            field=filer.fields.image.FilerImageField(related_name='profile_thumbnail', on_delete=django.db.models.deletion.SET_NULL, default=None, to='filer.Image', blank=True, help_text='Image must be 1:1 aspect ratio', null=True, verbose_name='Thumbnail Image'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='profile',
            order_with_respect_to='profile_plugin',
        ),
    ]
