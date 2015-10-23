from django.conf import settings

STATIC_URL = getattr(settings, 'STATIC_URL')
MAX_PROFILE_LINKS = getattr(settings, 'CMSPLUGIN_PROFILE_NR_LINKS', 4)
