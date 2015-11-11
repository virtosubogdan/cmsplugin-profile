from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin.templatetags.admin_static import static

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import (
    ProfileForm, ProfileFormSet, SelectedProfileForm, SelectedProfileFormSet,
    ProfileGridPromoForm, ProfileGridForm
)
from .models import Profile, ProfileGrid, SelectedProfile, ProfilePromoGrid
from .settings import INITIAL_DISPLAYED_PROFILES


class ProfileInline(admin.options.InlineModelAdmin):
    model = Profile
    template = "admin/profile/profiles_inline.html"
    form = ProfileForm
    formset = ProfileFormSet
    extra = 0


class ProfileGridPlugin(CMSPluginBase):
    inlines = (ProfileInline, )
    model = ProfileGrid
    name = "Profile Grid"
    render_template = 'cmsplugin_profile/profilegrid_plugin.html'
    change_form_template = "admin/profile/profilegrid_change_form.html"
    admin_preview = False
    form = ProfileGridForm

    def render(self, context, instance, placeholder):
        context['profilegrid'] = instance
        context['profiles'] = instance.profile_set.all()
        context['initial_displayed_profile'] = INITIAL_DISPLAYED_PROFILES
        return context

    @property
    def media(self):
        media_obj = super(ProfileGridPlugin, self).media

        media_obj.add_css({
            'all': (
                static('admin/css/profile_admin.css'), )
        })
        media_obj.add_js((
            static('admin/js/lib/jquery-ui.min.js'),
            static('admin/js/profile_admin.js'),
        ))

        return media_obj

plugin_pool.register_plugin(ProfileGridPlugin)


class SelectedProfileInline(admin.options.InlineModelAdmin):
    model = SelectedProfile
    template = "admin/profile/selectedprofiles_inline.html"
    form = SelectedProfileForm
    formset = SelectedProfileFormSet


class ProfileGridPromoPlugin(CMSPluginBase):
    model = ProfilePromoGrid
    name = "Profile Grid Promo"
    render_template = 'cmsplugin_profile/profilegridpromo_plugin.html'
    change_form_template = "admin/profile/profilegridpromo_change_form.html"
    admin_preview = False
    form = ProfileGridPromoForm

    fieldsets = (
        (None, {
            'fields': ('profile_plugin', 'title', 'call_to_action_text'),
        }),
        ("Featured Profiles", {
            'fields': ('profiles_field', ),
            'description': _(u'Three profiles will...'),
        })
    )

    @property
    def media(self):
        media_obj = super(ProfileGridPromoPlugin, self).media

        media_obj.add_css({
            'all': (
                static('admin/css/profile_admin.css'), )
        })
        media_obj.add_js((
            static('admin/js/lib/jquery-ui.min.js'),
        ))

        return media_obj

    def get_form(self, request, obj=None, **kwargs):
        form_class = super(ProfileGridPromoPlugin, self).get_form(
            request, obj, **kwargs)

        class MetaFormClass(form_class):
            def __new__(cls, *args, **kwargs):
                kwargs.update({"request": request})
                return form_class(*args, **kwargs)

        return MetaFormClass

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(ProfileGridPromoPlugin)
