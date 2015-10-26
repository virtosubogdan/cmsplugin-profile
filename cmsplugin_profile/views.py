from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied
from django.template import RequestContext

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
        print paginator.page(page)
        print paginator.page(page).object_list
        for profile in paginator.page(page).object_list:
            response['profiles'].append(
                [profile.id, profile.title, profile.description, profile.thumbnail_image.url]
            )
    return JsonResponse(response)


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
