from django import forms
from django.core.exceptions import ValidationError

from cms_blogger.widgets import ToggleWidget

from .models import Profile, ProfileLink, ProfileGrid, SelectedProfile, ProfilePromoGrid
from .settings import MAX_PROFILE_LINKS


class ProfileForm(forms.ModelForm):
    max_profile_links = MAX_PROFILE_LINKS

    class Meta:
        model = Profile
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.links = [(index+1, link)
                          for index, link in enumerate(self.instance.profilelink_set.all())]
            self.empty_links = range(len(self.links)+1, self.max_profile_links+1)
        else:
            self.links = []
            self.empty_links = range(1, self.max_profile_links+1)

        self.links_len = len(self.links) + 1
        self.links_prefix = self.add_prefix("links_set-")

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()

        for link_index in range(1, self.max_profile_links+1):
            prefix = self.add_prefix("links_set-{}-".format(link_index))
            text = self.data.get("{}text".format(prefix))
            url = self.data.get("{}url".format(prefix))
            open_action = self.data.get("{}open_action".format(prefix))
            if not text and not url:
                continue
            if not text:
                raise ValidationError("Link text is mandatory!")
            if not url:
                raise ValidationError("Link URL is mandatory!")
            if not open_action or open_action not in ("blank", "parent"):
                raise ValidationError("Please select a target for the link!")
            if "links" not in cleaned_data:
                cleaned_data["links"] = []
            cleaned_data["links"].append((link_index, text, url, open_action))
        if not self.instance.id:
            cleaned_data['not_saved_profile'] = self.instance
        return cleaned_data


def _add_links_to_profile(profile, links_data, commit=True):
    # TODO: add link ordering and do not delete only what has to be deleted
    if not commit:
        # We cannot modify related objects for unsaved object
        return
    profile.profilelink_set.all().delete()
    for _, text, url, target in links_data:
        ProfileLink.objects.create(profile=profile, text=text, url=url, target=target)


class ProfileFormSet(forms.models.BaseInlineFormSet):

    def save(self, commit=True):
        result = super(ProfileFormSet, self).save(commit)

        for profile_data in self.cleaned_data:
            profile = profile_data.get('id', None) or profile_data.get("not_saved_profile", None)
            if not profile or (profile not in self.queryset and profile not in result):
                continue
            _add_links_to_profile(profile, profile_data.get("links", []), commit=commit)

        return result


class SelectedProfileForm(forms.ModelForm):

    class Meta:
        model = SelectedProfile
        exclude = ()


class SelectedProfileFormSet(forms.models.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(SelectedProfileFormSet, self).__init__(*args, **kwargs)
        if self.instance:
            self.selected_profiles = [sel.profile for sel in self.instance.selected_profiles.all()]
            self.available_profiles = [profile
                                       for profile
                                       in self.instance.profile_plugin.profile_set.all()
                                       if profile not in self.selected_profiles]
        else:
            self.available_profiles = []
            self.selected_profiles = []


class ProfileGridForm(forms.ModelForm):
    show_title_on_thumbnails = forms.BooleanField(
        label="Show title on thumbnails",
        widget=ToggleWidget,
        required=False
    )

    class Meta:
        model = ProfileGrid
        exclude = ()


class ProfileGridPromoForm(forms.ModelForm):
    selectable_profiles = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    class Meta:
        model = ProfilePromoGrid
        exclude = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileGridPromoForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.selected_profiles = [
                selected_profile for selected_profile in self.instance.selected_profiles.all()
            ]
            self.all_profiles = self.instance.profile_plugin.profile_set.all()
        else:
            self.selected_profiles = []
            self.all_profiles = []
            self.fields['selectable_profiles'].required = False

        selectable_profiles = self.fields['selectable_profiles']
        selectable_profiles.choices = [
            (profile.id, profile.id)
            for profile in self.all_profiles
        ]
        selectable_profiles.initial = [
            selected_profile.id
            for selected_profile in self.selected_profiles
        ]
        self.fields['profile_plugin'].queryset = ProfileGrid.objects.filter(
            placeholder__page__site_id=self.request.current_page.site_id
        )

    def save(self, commit=True):
        ret_value = super(ProfileGridPromoForm, self).save(commit=commit)
        self.instance.selectedprofile_set.all().delete()
        for profile_id in self.cleaned_data['selectable_profiles']:
            profile = Profile.objects.get(id=int(profile_id))
            SelectedProfile.objects.create(profile=profile, promo_grid=self.instance)
        return ret_value
