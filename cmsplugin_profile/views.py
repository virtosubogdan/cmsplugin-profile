from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms import HiddenInput
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied
from django.template import RequestContext

from cms.utils.permissions import has_plugin_permission

from .forms import ProfileForm
from .models import ProfileGrid


@require_GET
def view_profiles(request, profilegrid_id):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        max_results = int(request.GET.get('max_results', 4))
    except:
        max_results = 4
    if not request.user.is_authenticated():
        raise PermissionDenied
    profile_grid = get_object_or_404(ProfileGrid, id=profilegrid_id)
    paginator = Paginator(profile_grid.profile_set.all(), max_results)
    response = {
        'profiles': [],
        'has_more': (page < paginator.num_pages),
        'max_pages': paginator.num_pages
    }
    if page <= paginator.num_pages:
        for profile in paginator.page(page).object_list:
            response['profiles'].append(
                _serialize_profile(profile)
            )
    return JsonResponse(response)


def _serialize_profile(profile):
    return {
        "id": profile.id,
        "detail_image": profile.detail_image.url,
        "thumbnail_image": profile.thumbnail_image.url,
        "image_credit": profile.image_credit,
        "title": profile.title,
        "description": profile.description,
        "call_to_action_text": profile.call_to_action_text,
        "call_to_action_url": profile.call_to_action_url,
        "additional_links_label": profile.additional_links_label,
        "links": [
            {
                "text": link.text, "url": link.url, "target": link.target
            } for link in profile.profilelink_set.all()
        ]
    }


@require_GET
def new_profile(request, profile_nr):
    if not has_plugin_permission(request.user, "ProfileGridPlugin", "change"):
        raise PermissionDenied
    grid_id = request.GET.get("profilegrid_id", None)
    form = ProfileForm(
        auto_id='id_%s',
        prefix=u'profile_set-{}'.format(profile_nr),
        empty_permitted=True
    )
    grid_field = form.fields['profile_plugin']
    grid_field.widget = HiddenInput()
    grid_field.initial = grid_id
    return render_to_response(
        'admin/profile/profile_form.html',
        {'form': form},
        RequestContext(request)
    )
