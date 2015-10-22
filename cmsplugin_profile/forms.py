from django import forms
from django.core.exceptions import ValidationError

from .models import Profile, ProfileLink
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
            if not "links" in cleaned_data:
                cleaned_data["links"] = []
            cleaned_data["links"].append((link_index, text, url, open_action))
        return cleaned_data


class ProfileFormSet(forms.models.BaseInlineFormSet):

    def save(self, commit=True):
        result = super(ProfileFormSet, self).save(commit)
        for item in self.cleaned_data:
            try:
                profile = item.get('id')
            except:
                continue
            if profile not in self.queryset:
                continue
            profile.profilelink_set.all().delete()
            links = item.get("links", [])
            for _, text, url, target in links:
                ProfileLink.objects.create(profile=profile, text=text, url=url, target=target)
        return result
