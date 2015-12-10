from django import forms
from django.core.exceptions import ValidationError

from .compatibility import ToggleWidget
from .models import Profile, ProfileLink, ProfileGrid, SelectedProfile, ProfilePromoGrid
from .settings import MAX_PROFILE_LINKS, MAX_PROMO_PROFILES


class ProfileForm(forms.ModelForm):
    max_profile_links = MAX_PROFILE_LINKS

    class Meta:
        model = Profile
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._customize_image_widgets()
        self._make_link_data()

    def _customize_image_widgets(self):
        img_widgets = [self.fields['thumbnail_image'].widget, self.fields['detail_image'].widget]
        for img_widget in img_widgets:
            img_widget.can_delete_related = False
            if hasattr(img_widget, 'widget'):
                img_widget = img_widget.widget
            img_widget.custom_preview_width = 200
            img_widget.search_label = "Upload from Filer"
            img_widget.remove_label = "Remove"

    def _make_link_data(self):
        self.links_text_max_length = ProfileLink._meta.get_field("text").max_length
        self.links_url_max_length = ProfileLink._meta.get_field("url").max_length
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
            deleted = self.data.get("{}delete".format(prefix))
            if deleted:
                continue
            if not text and not url:
                continue
            self._validate_link(text, url, open_action)
            if "links" not in cleaned_data:
                cleaned_data["links"] = []
            cleaned_data["links"].append((link_index, text, url, open_action))
        if not self.instance.id:
            cleaned_data['not_saved_profile'] = self.instance

        return cleaned_data

    def _validate_link(self, text, url, open_action):
        if not text:
            raise ValidationError("Link text is mandatory!")
        if not url:
            raise ValidationError("Link URL is mandatory!")
        if " " in url:
            raise ValidationError("Link URL must not contain spaces!")
        if not any(url.startswith(start) for start in ["/", "http://", "https://"]):
            raise ValidationError("Link URL must start with http(s):// or / !")
        if not open_action or open_action not in ("blank", "same window"):
            raise ValidationError("Please select a target for the link!")


def _add_links_to_profile(profile, links_data, commit=True):
    # TODO: add link ordering and do not delete only what has to be deleted
    if not commit:
        # We cannot modify related objects for unsaved object
        return
    profile.profilelink_set.all().delete()
    for _, text, url, target in links_data:
        ProfileLink.objects.create(profile=profile, text=text, url=url, target=target)


class ProfileFormSet(forms.models.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.can_order = True
        super(ProfileFormSet, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        result = super(ProfileFormSet, self).save(commit)

        for profile_data in self.cleaned_data:
            profile = profile_data.get('id', None) or profile_data.get("not_saved_profile", None)
            if not profile or (profile not in self.queryset and profile not in result):
                continue
            _add_links_to_profile(profile, profile_data.get("links", []), commit=commit)

        ordered_pks = [f.instance.pk for f in self.ordered_forms]
        if self.instance.get_profile_order() != ordered_pks:
            self.instance.set_profile_order(ordered_pks)

        return result


class ProfileGridForm(forms.ModelForm):
    show_title_on_thumbnails = forms.BooleanField(
        label="Show title on thumbnails",
        widget=ToggleWidget,
        required=False
    )

    class Meta:
        model = ProfileGrid
        exclude = ()


class SelectedProfilesField(forms.Field):

    def to_python(self, value):
        if not value:
            return []
        try:
            return [int(id_val) for id_val in value.split(",")]
        except ValueError:
            raise forms.ValidationError("Invalid list of selected profiles!")


class ProfileGridPromoForm(forms.ModelForm):
    profiles_field = SelectedProfilesField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = ProfilePromoGrid
        exclude = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileGridPromoForm, self).__init__(*args, **kwargs)

        self._load_custom_data()
        self._set_values_for_fields()
        if self.request.method == "POST":
            self._load_post_data()

    def _load_post_data(self):
        """
        For POST request transform the request into custom form data so if the validation
        fails, the template rendered to the user will contain the changes that were made
        to the custom fields.
        """
        selected_profile_ids = self.data.get('profiles_field', '').split(',')
        self.all_profiles = [
            (profile, str(profile.id) in selected_profile_ids)
            for profile, _ in self.all_profiles
        ]

    def _load_custom_data(self):
        self.changed_grid = self._get_changed_grid()
        if self.changed_grid and not (
                self.instance.id and self.instance.profile_plugin.id == self.changed_grid.id):
            self.selected_profiles = []
            self.all_profiles = [
                (profile, False)
                for profile in self.changed_grid.profile_set.all()
            ]
        elif self.instance.id:
            self.selected_profiles = [
                selected_profile for selected_profile in self.instance.selected_profiles.all()
            ]
            self.all_profiles = [
                (profile, profile in self.selected_profiles)
                for profile in self.instance.profile_plugin.profile_set.all()
            ]
        else:
            self.selected_profiles = []
            self.all_profiles = []
        self.maximum_selection = MAX_PROMO_PROFILES

    def _get_changed_grid(self):
        if not self.request:
            return None
        grid_param = self.request.GET.get("profile_grid", None)
        if not grid_param:
            return None
        try:
            return ProfileGrid.objects.get(
                id=grid_param,
                placeholder__page__site_id=self.request.current_page.site_id
            )
        except ProfileGrid.DoesNotExist:
            return None

    def _set_values_for_fields(self):
        profiles_field = self.fields['profiles_field']
        profiles_field.initial = ','.join([
            str(selected_profile.id)
            for selected_profile in self.selected_profiles
        ])
        self.fields['profile_plugin'].queryset = ProfileGrid.objects.filter(
            placeholder__page__site_id=self.request.current_page.site_id
        )
        if self.changed_grid:
            # Since form.initial dict takes priority over field.initial value and we
            # can have initial data on the form because we can have an instance, we
            # must do things this way.
            self.initial['profile_plugin'] = self.changed_grid.id

    def clean(self):
        cleaned_data = super(ProfileGridPromoForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        self.instance.unsaved_selected_profiles = []
        for profile_id in self.cleaned_data['profiles_field']:
            profile = Profile.objects.get(id=int(profile_id))
            selected_profile = SelectedProfile(profile=profile, promo_grid=self.instance)
            self.instance.unsaved_selected_profiles.append(selected_profile)
        return super(ProfileGridPromoForm, self).save(commit=commit)
