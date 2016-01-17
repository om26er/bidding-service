from django.http import Http404

from login.models import(
    CustomUser,
    ProductAd,
    Bids,
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


def _send_push_notification(message, reg_ids):
    from gcm import GCM
    gcm = GCM('AIzaSyDvMYsVLk80XXo_omD7mjS1TfzTNDQkqFk')
    data = {'message': message}
    gcm.plaintext_request(registration_ids=reg_ids, data=data)


def _really_delete(pk):
    """Delete an ad by primary key and send a push notification."""
    ad = ProductAd.objects.get(pk=pk)
    ad.delete()
    reg_ids = [
        'cooGNSL0diU:APA91bGiLL3oJmeZ0Dt2_AsskSKOQQ8HfsIbZQ_J7yug96pSgx5oiNiUt'
        'PcfAI8mZ86I6FJXFxdXP0C5afNnUDlzbp4F8LZOOAaOKB9MgYIDo3OrGCmn6G_kC7GiUx'
        '2TvCDTfBVEWqo8'
    ]
    _send_push_notification('Ad expired', reg_ids=reg_ids)


def delete_ad(pk, delay):
    """Delete an ad with a delay."""
    import threading
    t = threading.Timer(float(delay), _really_delete, args=(pk,))
    t.start()


def send_push_by_subscribed_categories(message_text, category):
    users = CustomUser.objects.filter(
        interests__in=category, is_active=True)
    push_ids = []
    for user in users:
        push_ids.append(user.push_key)
    _send_push_notification(message_text, reg_ids=push_ids)


def did_someone_bid(pk):
    ad = ProductAd.objects.get(pk=pk)
    # return len(ad.)


def get_user_id_by_name(username):
    try:
        return CustomUser.objects.get(username=username).id
    except CustomUser.DoesNotExist:
        raise Http404


def did_user_already_bid(ad_id, bidder_id):
    bids = Bids.objects.filter(ad_id=ad_id, bidder_id=bidder_id)
    return len(bids) > 0
