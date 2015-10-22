from django.conf import settings


MAX_PROFILE_LINKS = getattr(settings, 'CMSPLUGIN_PROFILE_NR_LINKS', 4)
