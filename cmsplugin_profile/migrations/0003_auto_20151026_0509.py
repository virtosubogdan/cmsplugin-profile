# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_profile', '0002_profilelink_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='additional_links_label',
            field=models.CharField(default=b'', max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profilegrid',
            name='description',
            field=models.TextField(default=b'', max_length=400),
        ),
        migrations.AlterField(
            model_name='profile',
            name='call_to_action_text',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(max_length=395, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image_credit',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profilelink',
            name='text',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
