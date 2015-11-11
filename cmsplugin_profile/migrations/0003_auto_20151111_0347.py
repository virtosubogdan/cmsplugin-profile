# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_profile', '0002_auto_20151111_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilegrid',
            name='load_mode_type',
            field=models.CharField(default='load_more_button', help_text='Button loading will load more profiles when the user clicks the button.Use this when the grid will be in a page with other elements. Scroll loaging will load more profiles when the user scrolls the page.Use this when the grid will be alone on the page.', max_length=20, verbose_name='Loading type', choices=[(b'load_mode_button', 'BUTTON'), (b'load_mode_scroll', 'SCROLL')]),
            preserve_default=False,
        ),
    ]
