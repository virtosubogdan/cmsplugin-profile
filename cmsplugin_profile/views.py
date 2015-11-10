from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms import HiddenInput
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import PermissionDenied
from django.template import RequestContext

from filer.models import Image

from .forms import ProfileForm
from .models import ProfileGrid, Profile, ProfileLink
from .settings import MAX_PROFILE_LINKS


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
    form = ProfileForm(
        auto_id='id_%s',
        prefix=u'profile_set-{}'.format(profile_nr),
        empty_permitted=True
    )
    form.fields['profile_plugin'].widget = HiddenInput()
    return render_to_response(
        'admin/profile/profile_form.html',
        {'form': form},
        RequestContext(request)
    )


@require_POST
def delete_profile(request, profile_id):
    try:
        Profile.objects.get(id=profile_id).delete()
        status = "ok"
    except Exception:
        status = "failed"

    return JsonResponse({"status": status})


class ValidationException(Exception):
    pass


def _clean_links(data):
    links = []
    for index in range(1, MAX_PROFILE_LINKS):
        text = data.get("link-{}-text".format(index), None)
        url = data.get("link-{}-url".format(index), None)
        target = data.get("link-{}-target".format(index), None)
        delete = data.get("link-{}-delete".format(index), None)
        if delete:
            pass
        if text and url:
            links.append(ProfileLink(text=text, url=url, target=target))
    return links


def _clean_profile_data(data):
    if "id" not in data or not data["id"]:
        profile_id = None
    else:
        try:
            profile_id = int(data["id"])
        except ValueError:
            raise ValidationException("Invalid value id:{} for profile id!".format(data["id"]))

    def _get_value_or_exception(val_name, allow_none=False):
        value = data.get(val_name, None)
        if not allow_none and not value:
            raise ValidationException("Missing {} attribute".format(val_name))
        return value

    cleaned_data = {
        "title": _get_value_or_exception("title"),
        "description": _get_value_or_exception("description"),
        "call_to_action_text": _get_value_or_exception("call_to_action_text", True),
        "call_to_action_url": _get_value_or_exception("call_to_action_url", True),
        "additional_links_label": _get_value_or_exception("additional_links_label", True),
        "image_credit": _get_value_or_exception("image_credit", True),
        "links": _clean_links(data),
    }

    try:
        img_id = int(data["thumbnail_image"])
        cleaned_data["thumbnail_image"] = Image.objects.get(id=img_id)
    except Exception as ex:
        print ex
        cleaned_data["thumbnail_image"] = None

    try:
        img_id = int(data["detail_image"])
        cleaned_data["detail_image"] = Image.objects.get(id=img_id)
    except:
        cleaned_data["detail_image"] = None

    return profile_id, cleaned_data


@require_POST
def save_profile(request, profilegrid_id):
    get_object_or_404(ProfileGrid, id=profilegrid_id)
    data = dict(request.POST.dict())

    try:
        profile_id = data.get("id", "")
        profile = get_object_or_404(Profile, id=profile_id) if profile_id else None
    except ValueError:
        return JsonResponse({
            "status": "failed",
            "error": "Invalid value for profile_id",
        })

    data['profile_plugin'] = profilegrid_id
    form = ProfileForm(prefix="", data=data, instance=profile)
    if form.errors:
        response = JsonResponse({
            "status": "failed",
            "error": form.errors,
        })
        return response
    profile = form.save()

    return JsonResponse({
        "status": "ok",
        "error": "",
        "id": profile.id,
    })
