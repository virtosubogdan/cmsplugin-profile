from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied

from .forms import ProfileForm
from .models import ProfileGrid


@require_GET
def view_profiles(request, profilegrid_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    profile_grid = get_object_or_404(ProfileGrid, id=profilegrid_id)
    print profile_grid
    return HttpResponse(str(profile_grid))


@require_GET
def new_profile(request, profile_nr):
    form = ProfileForm(
        auto_id='id_%s',
        prefix=u'profile_set-{}'.format(profile_nr),
        empty_permitted=True
    )
    del form.fields['profile_plugin']
    return HttpResponse(form.as_p())
