from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


class ProfileGrid(CMSPlugin):
    title = models.CharField(null=True, blank=True, max_length=200)
    show_title_on_thumbnails = models.BooleanField(default=False)

    class Meta:
        db_table = 'cmsplugin_profilegrid'


class Profile(models.Model):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    title = models.CharField(null=True, blank=True, max_length=200)
    description = models.CharField(null=True, blank=True, max_length=395)
    call_to_action_text = models.CharField(null=True, blank=True, max_length=200)
    call_to_action_url = models.CharField(null=True, blank=True, max_length=200)
    thumbnail_image = FilerImageField(
        null=True, blank=True, on_delete=models.SET_NULL,
        default=None, help_text=_('Image must be 1:1 aspect ratio'),
        verbose_name=_("Thumbnail Image"))
    image_credit = models.CharField(null=True, blank=True, max_length=200)


class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    text = models.CharField(null=True, blank=True, max_length=200)
    url = models.CharField(null=True, blank=True, max_length=200)
    target = models.CharField(null=True, blank=True, max_length=50)


class ProfilePromoGrid(CMSPlugin):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    selected_profiles = models.ManyToManyField(
        Profile, through="SelectedProfile", through_fields=('promo_grid', 'profile')
    )
    title = models.CharField(null=True, blank=True, max_length=200)
    call_to_action_text = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        db_table = 'cmsplugin_profilepromogrid'


class SelectedProfile(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    promo_grid = models.ForeignKey(ProfilePromoGrid, null=False, blank=False)

