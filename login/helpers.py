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
        # api_view.check_object_permissions(request, obj)
        return obj
    except ProductAd.DoesNotExist:
        raise Http404


def does_user_exist(username):
    """
    Return bool representing if the requested user is already registered.
    """
    try:
        CustomUser.objects.get(username=username)
        return True
    except CustomUser.DoesNotExist:
        return False


def _send_push_notification(message):
    from gcm import GCM
    gcm = GCM('AIzaSyDvMYsVLk80XXo_omD7mjS1TfzTNDQkqFk')
    reg_id = 'cooGNSL0diU:APA91bGiLL3oJmeZ0Dt2_AsskSKOQQ8HfsIbZQ_J7yug96' \
             'pSgx5oiNiUtPcfAI8mZ86I6FJXFxdXP0C5afNnUDlzbp4F8LZOOAaOKB9M' \
             'gYIDo3OrGCmn6G_kC7GiUx2TvCDTfBVEWqo8'
    data = {'message': message}
    gcm.plaintext_request(registration_id=reg_id, data=data)


def _really_delete(pk):
    """Delete an ad by primary key and send a push notification."""
    ad = ProductAd.objects.get(pk=pk)
    ad.delete()
    _send_push_notification('Ad expired')


def delete_ad(pk, delay):
    """Delete an ad with a delay."""
    import threading
    t = threading.Timer(float(delay), _really_delete, args=(pk,))
    t.start()
