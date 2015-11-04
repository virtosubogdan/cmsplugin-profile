from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


class ProfileGrid(CMSPlugin):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, max_length=400, default="")
    show_title_on_thumbnails = models.BooleanField(default=False)

    class Meta:
        db_table = 'cmsplugin_profilegrid'


class Profile(models.Model):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    title = models.CharField(null=True, blank=True, max_length=200)
    description = models.TextField(max_length=395)
    call_to_action_text = models.CharField(null=True, blank=True, max_length=30)
    call_to_action_url = models.CharField(null=True, blank=True, max_length=200)
    additional_links_label = models.CharField(null=True, blank=True, max_length=30, default="")
    thumbnail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio'),
        verbose_name=_("Thumbnail Image"),
        related_name="profile_thumbnail"
    )
    detail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio'),
        verbose_name=_("Detail Image"),
        related_name="profile_detail"
    )
    image_credit = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        order_with_respect_to = 'profile_plugin'


class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    text = models.CharField(null=True, blank=True, max_length=60)
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
