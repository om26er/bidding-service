from django.http import Http404

from login.models import(
    CustomUser,
    ProductAd,
)


def get_user_by_username(api_view, request, username):
    try:
        obj = CustomUser.objects.get(username=username)
        api_view.check_object_permissions(request, obj)
        return obj
    except CustomUser.DoesNotExist:
        raise Http404


def get_ad_by_primary_key(api_view, request, pk):
    try:
        obj = ProductAd.objects.get(pk=pk)
        api_view.check_object_permissions(request, obj)
        return obj
    except ProductAd.DoesNotExist:
        raise Http404
