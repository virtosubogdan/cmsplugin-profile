from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import ProfileForm, ProfileFormSet
from .models import Profile, ProfileGrid, SelectedProfile, ProfilePromoGrid


class ProfileInline(admin.options.InlineModelAdmin):
    model = Profile
    template = "admin/profile/profiles_inline.html"
    form = ProfileForm
    formset = ProfileFormSet


class ProfileGridPlugin(CMSPluginBase):
    inlines = (ProfileInline, )
    model = ProfileGrid
    name = "Profile Grid"
    render_template = 'cmsplugin_profile/profilegrid_plugin.html'
    admin_preview = False

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(ProfileGridPlugin)


class SelectedProfileInline(admin.options.InlineModelAdmin):
    model = SelectedProfile
    template = "admin/profile/selectedprofiles_inline.html"


class ProfileGridPromoPlugin(CMSPluginBase):
    inlines = (SelectedProfileInline, )
    model = ProfilePromoGrid
    name = "Profile Grid Promo"
    render_template = 'cmsplugin_profile/profilegridpromo_plugin.html'
    change_form_template = "admin/profile/profilegridpromo_change_form.html"
    admin_preview = False

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(ProfileGridPromoPlugin)
