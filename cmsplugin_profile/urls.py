from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cmsplugin_profile.views',
    url(r'^cmsplugin_profile/(?P<profilegrid_id>\d+)/view_profiles/$',
        'view_profiles', name='view_profiles'),
    url(r'^cmsplugin_profile/new_profile/(?P<profile_nr>\d+)/$',
        'new_profile', name='new_profile'),
    url(r'^cmsplugin_profile/save_profile/(?P<profilegrid_id>\d+)/$',
        'save_profile', name='save_profile'),
)
