from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied
from django.template import RequestContext

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
    return render_to_response(
        'admin/profile/profile_form.html',
        {'form': form},
        RequestContext(request)
    )
