from login.models import CustomUser, ProductAd
from login.serializers import UserSerializer, AdSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.settings import AUTH_USER_MODEL


def _is_creator(username, request):
    return username == str(request.user)


class UsersList(APIView):

    def get(self, request, format=None):
        if not request.user.is_staff:
            return Response(
                data="Only Admin users allowed to get list of users",
                status=status.HTTP_403_FORBIDDEN
            )
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, username, request):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        if not _is_creator(username, request):
            return Response(data='Only the user can access their details',
                            status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(username, request)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        if not _is_creator(username, request):
            return Response(data='Only the user can change their details',
                            status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(username, request)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        if not _is_creator(username, request):
            return Response(data='Only the user can delete their self',
                            status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(username, request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExists(APIView):

    def get(self, request, format=None):
        user = request.data.get('username')
        if not user:
            return Response(data="'username' field not found in request",
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            CustomUser.objects.get(username=user)
            return Response(
                data='Yes, user: {}, already exists'.format(user),
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                data='User with name {}, does not exist'.format(user),
                status=status.HTTP_404_NOT_FOUND
            )


class Push(APIView):

    def post(self, request, format=None):
        _send_push_notification(request.data.get('message'))
        return Response(data='Notification Sent', status=status.HTTP_200_OK)


def _send_push_notification(message):
    from gcm import GCM
    gcm = GCM('AIzaSyDvMYsVLk80XXo_omD7mjS1TfzTNDQkqFk')
    reg_id = 'cooGNSL0diU:APA91bGiLL3oJmeZ0Dt2_AsskSKOQQ8HfsIbZQ_J7yug96' \
             'pSgx5oiNiUtPcfAI8mZ86I6FJXFxdXP0C5afNnUDlzbp4F8LZOOAaOKB9M' \
             'gYIDo3OrGCmn6G_kC7GiUx2TvCDTfBVEWqo8'
    data = {'message': message}
    gcm.plaintext_request(registration_id=reg_id, data=data)


class UserAdsView(APIView):

    def put(self, request, username, format=None):
        if str(request.user) != username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username, format=None):
        if str(request.user) != username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ads = ProductAd.objects.all()
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)


class UserAdView(APIView):

    def get_ad(self, pk):
        try:
            return ProductAd.objects.get(pk=pk)
        except ProductAd.DoesNotExist:
            raise Http404

    def get(self, request, username, pk, format=None):
        ad = self.get_ad(pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)


class AdsView(APIView):

    # def json_to_keyword_arguments(self, json_data):

    def get_ads(self, **kwargs):
        try:
            return ProductAd.objects.filter(**kwargs)
        except ProductAd.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        ads = self.get_ads(**request.data)
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)
