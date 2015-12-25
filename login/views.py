from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework import permissions

from login.models import(
    CustomUser,
    ProductAd,
)
from login.serializers import(
    UserSerializer,
    AdSerializer,
    UserInterestsSerializer,
    UserPushIdSerializer,
)
from login.permissions import IsOwner
from login import helpers


class RegistrationView(CreateAPIView):

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update the password so that its hashed.
            user = CustomUser.objects.get(username=request.POST['username'])
            user.set_password(request.POST['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return super().post(request, *args, **kwargs)


class UsersList(ListAPIView):

    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(APIView):

    permission_classes = (IsOwner,)

    def get(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExists(APIView):

    def get(self, request, username, format=None):
        try:
            CustomUser.objects.get(username=username)
            return Response(data='User: {}, already exists'.format(username),
                            status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data='User: {}, does not exist'.format(username),
                            status=status.HTTP_404_NOT_FOUND)


class UserPostAdView(APIView):

    def post(self, request, username, format=None):
        if request.user.username != username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            helpers.delete_ad(serializer.data.get('id'), 60)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdView(APIView):

    permission_classes = (IsOwner, )

    def get(self, request, username, pk, format=None):
        ad = helpers.get_ad_by_primary_key(self, request, pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)


class UserAdsList(ListAPIView):

    permission_classes = (IsOwner, )
    serializer_class = AdSerializer

    def get_queryset(self):
        return ProductAd.objects.filter(owner=self.request.user)


class AdsFilterView(ListAPIView):

    serializer_class = AdSerializer

    def get_queryset(self):
        # Convert the request from QueryDict to a dictionary
        query = self.request.GET.dict()
        return ProductAd.objects.filter(**query)


class InterestsView(APIView):

    permission_classes = (IsOwner, )

    def get(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        interests = user.get('interests')
        data = '{"interests": {}'.format(interests)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserInterestsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PushKeyView(APIView):

    permission_classes = (IsOwner, )

    def put(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserPushIdSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
