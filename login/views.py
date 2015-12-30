from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import(
    ListAPIView,
    CreateAPIView,
)
from rest_framework import status
from rest_framework import permissions

from login.models import(
    CustomUser,
    ProductAd,
    Comments,
)
from login.serializers import(
    UserSerializer,
    AdSerializer,
    UserInterestsSerializer,
    UserPushIdSerializer,
    AdCommentSerializer,
    AdCommentsSerializer
)
from login.permissions import IsOwner
from login import helpers


from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class RegistrationView(CreateAPIView):

    serializer_class = UserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update the password so that its hashed.
            user = CustomUser.objects.get(
                username=request.data.get('username'))
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # helpers.delete_ad(serializer.data.get('id'), 60)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdCommentCreateView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        ad = ProductAd.objects.get(id=kwargs.get('pk'))
        serializer = AdCommentSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdCommentsList(ListAPIView):

    def get(self, request, **kwargs):
        ad = ProductAd.objects.get(id=kwargs.get('pk'))
        comments = Comments.objects.filter(ad=ad)
        serializer = AdCommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdCommentView(APIView):

    def get(self, request, **kwargs):
        comment = Comments.objects.get(id=kwargs.get('comment_id'))
        serializer = AdCommentsSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        data = {"interests": user.interests}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserInterestsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PushKeyView(APIView):

    permission_classes = (IsOwner, )

    def post(self, request, username, format=None):
        user = helpers.get_user_by_username(self, request, username)
        serializer = UserPushIdSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
