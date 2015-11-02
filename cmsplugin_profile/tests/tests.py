from django.core.urlresolvers import reverse
from django.test import TestCase

from filer.models import Image

from cmsplugin_profile.models import Profile, ProfileGrid


class ProfilePluginTest(TestCase):
    def testStuff(self):
        pass

class APITest(TestCase):

    def _create_image(self, title="test_image"):
        return Image.objects.create(title=title)

    def api_create_new_profile(self, profile_grid_id, data={}):
        post_data = {
            "title": "title",
            "description": "description",
        }
        post_data.update(data)
        print data
        return self.client.post(
            reverse("save_profile", args=[profile_grid_id]),
            post_data
        )

    def test_correct_create(self):
        assert Profile.objects.all().count() == 0
        profile_grid = ProfileGrid.objects.create(title="")
        image = self._create_image()
        profile_data = {
            "title": "p1",
            "description": "d1",
            "thumbnail_image": image.id,
            }
        print self.api_create_new_profile(profile_grid.id, data=profile_data)
        assert Profile.objects.filter(
            title="p1", description="d1", profile_plugin=profile_grid,
            thumbnail_image=image
        ).exists()

    def test_correct_update(self):
        assert Profile.objects.all().count() == 0
        profile_grid = ProfileGrid.objects.create(title="")
        profile = Profile.objects.create(profile_plugin=profile_grid, title="test")
        profile_data = {
            "title": "updated",
            "description": "d1",
            "id": profile.id
            }
        print self.api_create_new_profile(profile_grid.id, data=profile_data)
        assert Profile.objects.filter(
            profile_plugin=profile_grid, title="updated", description="d1"
        ).exists()
        assert Profile.objects.all().count() == 1
