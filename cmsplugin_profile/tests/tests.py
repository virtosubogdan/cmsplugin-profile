from django.contrib.auth.models import Group, Permission

from filer.models import Image
from cms.test_utils.testcases import CMSTestCase


class ProfileGridTest(CMSTestCase):

    def _create_image(self, title="test_image"):
        return Image.objects.create(title=title)

    def test_get_new_profile(self):
        admin = self.get_superuser()
        profile_index = 11
        grid_id = 0
        with self.login_user_context(admin):
            response = self.client.get(
                '/cmsplugin_profile/new_profile/{}/'.format(profile_index),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 200
        assert 'id="profile_set-{}"'.format(profile_index) in response.content

    def test_get_new_profile_no_user(self):
        profile_index = 11
        grid_id = 0
        response = self.client.get(
            '/cmsplugin_profile/new_profile/{}/'.format(profile_index),
            {'profilegrid_id': grid_id}
        )
        assert response.status_code == 403

    def test_get_new_profile_admin_no_rights(self):
        admin_no_rights = self.get_staff_user_with_no_permissions()
        profile_index = 11
        grid_id = 0
        with self.login_user_context(admin_no_rights):
            response = self.client.get(
                '/cmsplugin_profile/new_profile/{}/'.format(profile_index),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 403

    def test_get_new_profile_admin_rights(self):
        admin = self.get_staff_user_with_no_permissions()
        profile_index = 11
        grid_id = 0
        group = Group.objects.create(name="editor")
        group.user_set.add(admin)
        group.permissions.add(Permission.objects.get(name="Can change profile grid"))
        group.save()
        with self.login_user_context(admin):
            response = self.client.get(
                '/cmsplugin_profile/new_profile/{}/'.format(profile_index),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 200
        assert 'id="profile_set-{}"'.format(profile_index) in response.content
