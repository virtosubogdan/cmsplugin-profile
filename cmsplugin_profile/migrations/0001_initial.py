# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, null=True, blank=True)),
                ('description', models.TextField(max_length=395)),
                ('call_to_action_text', models.CharField(max_length=30, null=True, blank=True)),
                ('call_to_action_url', models.CharField(max_length=200, null=True, blank=True)),
                ('additional_links_label', models.CharField(default=b'', max_length=30, null=True, blank=True)),
                ('image_credit', models.CharField(max_length=40, null=True, blank=True)),
                ('detail_image', filer.fields.image.FilerImageField(related_name='profile_detail', on_delete=django.db.models.deletion.PROTECT, default=None, verbose_name='Detail Image', to='filer.Image', help_text='Image must be 1:1 aspect ratio. We recommend 600px min size.')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileGrid',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(default=b'', max_length=400, null=True, blank=True)),
                ('show_title_on_thumbnails', models.BooleanField(default=False)),
                ('load_mode_type', models.CharField(default=(b'load_mode_button', 'Load more button'), help_text='Button loading will load more profiles when the user clicks the button.Use this when the grid will be in a page with other elements. Scroll loaging will load more profiles when the user scrolls the page.Use this when the grid will be alone on the page.', max_length=20, verbose_name='Pagination type', choices=[(b'load_mode_button', 'Load more button'), (b'load_mode_scroll', 'Lazy loading')])),
            ],
            options={
                'db_table': 'cmsplugin_profilegrid',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ProfileLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=60, null=True, blank=True)),
                ('url', models.CharField(max_length=200, null=True, blank=True)),
                ('target', models.CharField(max_length=50, null=True, blank=True)),
                ('profile', models.ForeignKey(to='cmsplugin_profile.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePromoGrid',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=60, null=True, blank=True)),
                ('call_to_action_text', models.CharField(max_length=100)),
                ('profile_plugin', models.ForeignKey(to='cmsplugin_profile.ProfileGrid')),
            ],
            options={
                'db_table': 'cmsplugin_profilepromogrid',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='SelectedProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile', models.ForeignKey(to='cmsplugin_profile.Profile')),
                ('promo_grid', models.ForeignKey(to='cmsplugin_profile.ProfilePromoGrid')),
            ],
        ),
        migrations.AddField(
            model_name='profilepromogrid',
            name='selected_profiles',
            field=models.ManyToManyField(to='cmsplugin_profile.Profile', through='cmsplugin_profile.SelectedProfile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_plugin',
            field=models.ForeignKey(to='cmsplugin_profile.ProfileGrid'),
        ),
        migrations.AddField(
            model_name='profile',
            name='thumbnail_image',
            field=filer.fields.image.FilerImageField(related_name='profile_thumbnail', on_delete=django.db.models.deletion.PROTECT, default=None, verbose_name='Thumbnail Image', to='filer.Image', help_text='Image must be 1:1 aspect ratio. We recommend 440px min size.'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='profile',
            order_with_respect_to='profile_plugin',
        ),
    ]
