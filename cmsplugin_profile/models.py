from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


LOAD_MORE_BUTTON = "load_mode_button"
LOAD_MORE_SCROLL = "load_mode_scroll"
GRID_LOADING_TYPE_CHOICES = (
    (LOAD_MORE_BUTTON, _("Load more button")),
    (LOAD_MORE_SCROLL, _("Lazy loading")),
)


class ProfileGrid(CMSPlugin):
    title = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True, max_length=400, default="")
    show_title_on_thumbnails = models.BooleanField(default=False)
    load_mode_type = models.CharField(
        _("Pagination type"), max_length=20,
        choices=GRID_LOADING_TYPE_CHOICES,
        help_text=_("Button loading will load more profiles when the user clicks the button."
                    "Use this when the grid will be in a page with other elements. "
                    "Scroll loaging will load more profiles when the user scrolls the page."
                    "Use this when the grid will be alone on the page."),
        default=GRID_LOADING_TYPE_CHOICES[0])

    class Meta:
        db_table = 'cmsplugin_profilegrid'

    def __unicode__(self):
        return u'{}'.format(self.title)


class Profile(models.Model):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    title = models.CharField(null=True, blank=True, max_length=60)
    description = models.TextField(max_length=395)
    call_to_action_text = models.CharField(null=True, blank=True, max_length=30)
    call_to_action_url = models.CharField(null=True, blank=True, max_length=200)
    additional_links_label = models.CharField(null=True, blank=True, max_length=30, default="")
    thumbnail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio. We recommend 440px min size.'),
        verbose_name=_("Thumbnail Image"),
        related_name="profile_thumbnail"
    )
    detail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio. We recommend 600px min size.'),
        verbose_name=_("Detail Image"),
        related_name="profile_detail"
    )
    image_credit = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        order_with_respect_to = 'profile_plugin'

    def __unicode__(self):
        return u'{}'.format(self.title)

    @property
    def links(self):
        return self.profilelink_set.all()


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
    title = models.CharField(null=True, blank=True, max_length=60)
    call_to_action_text = models.CharField(max_length=100)

    class Meta:
        db_table = 'cmsplugin_profilepromogrid'

    def __unicode__(self):
        return u'{}'.format(self.title)

    def save(self, *args, **kwargs):
        ret_value = super(ProfilePromoGrid, self).save(*args, **kwargs)
        for unsaved_selected_profile in self.unsaved_selected_profiles:
            unsaved_selected_profile.promo_grid = self
            unsaved_selected_profile.save()
        return ret_value


class SelectedProfile(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    promo_grid = models.ForeignKey(ProfilePromoGrid, null=False, blank=False)
