# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilegrid',
            name='load_mode_type',
            field=models.CharField(choices=[(b'load_mode_button', 'BUTTON'), (b'load_mode_scroll', 'SCROLL')], max_length=10, blank=True, help_text='Button loading will load more profiles when the user clicks the button.Use this when the grid will be in a page with other elements. Scroll loaging will load more profiles when the user scrolls the page.Use this when the grid will be alone on the page.', null=True, verbose_name='Loading type'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='detail_image',
            field=filer.fields.image.FilerImageField(related_name='profile_detail', on_delete=django.db.models.deletion.PROTECT, default=None, verbose_name='Detail Image', to='filer.Image', help_text='Image must be 1:1 aspect ratio. We recommend 600px min size.'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='thumbnail_image',
            field=filer.fields.image.FilerImageField(related_name='profile_thumbnail', on_delete=django.db.models.deletion.PROTECT, default=None, verbose_name='Thumbnail Image', to='filer.Image', help_text='Image must be 1:1 aspect ratio. We recommend 440px min size.'),
        ),
    ]
