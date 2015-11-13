# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_profile', '0006_auto_20151113_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilegrid',
            name='title',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='profilepromogrid',
            name='call_to_action_text',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profilepromogrid',
            name='title',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
