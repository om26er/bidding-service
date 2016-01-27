from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import(
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework import permissions

from login.models import(
    CustomUser,
    ProductAd,
    Bids,
    AdCategories,
    Messages,
)
from login.serializers import(
    UserSerializer,
    AdSerializer,
    UserInterestsSerializer,
    UserPushIdSerializer,
    AdBidSerializer,
    AdCategoriesSerializer,
    BidsSerializer,
    MessagesSerializer
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


class CreateBidView(CreateAPIView):

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        username = str(self.request.user)
        user_id = helpers.get_user_id_by_name(username)
        ad_id = kwargs.get('pk')
        request.data.update({'ad': ad_id})
        request.data.update({'bidder': user_id})
        # Allow a user to bid only once per ad
        if helpers.did_user_already_bid(ad_id, user_id):
            return Response({'result': 'Only one bid per user per ad allowed'},
                            status=status.HTTP_409_CONFLICT)

        serializer = AdBidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdBidsView(ListAPIView):

    serializer_class = BidsSerializer

    def get_queryset(self):
        return Bids.objects.filter(ad_id=self.kwargs.get('pk'))


class GetUpdateDeleteBidView(RetrieveUpdateDestroyAPIView):

    serializer_class = AdBidSerializer

    def get_queryset_safe(self):
        from django.core.exceptions import ObjectDoesNotExist
        try:
            return self.get_queryset()
        except ObjectDoesNotExist:
            return None

    def get_queryset(self):
        return Bids.objects.get(id=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset_safe()
        if queryset:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'result': 'Comment does not exist'},
                        status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset_safe()
        if queryset:
            serializer = self.get_serializer(instance=queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data={'result': 'Comment does not exist'},
                        status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset_safe()
        if queryset:
            username = str(self.request.user)
            user_id = helpers.get_user_id_by_name(username)
            ad_id = kwargs.get('ad_id')
            request.data.update({'ad': ad_id})
            request.data.update({'bidder': user_id})
            serializer = self.get_serializer(instance=queryset,
                                             data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'result': 'Comment does not exist'},
                        status=status.HTTP_204_NO_CONTENT)


class UserBidsView(ListAPIView):

    serializer_class = AdSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        bids = Bids.objects.filter(bidder_id=self.request.user.id)
        return [bid.ad for bid in bids]


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
        page = query.get('page', None)
        if page:
            query.pop('page')
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


class CategoriesView(ListAPIView):

    serializer_class = AdCategoriesSerializer
    queryset = AdCategories.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MessagesView(ListCreateAPIView):

    serializer_class = MessagesSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Messages.objects.filter(ad_id=self.kwargs.get('pk'))

    def _get_direction(self, sender_name, ad_owner_name):
        if sender_name == ad_owner_name:
            return 'outgoing'
        return 'incoming'

    def post(self, request, **kwargs):
        sender_name = request.user.username
        direction = self._get_direction(sender_name,
                                        self.kwargs.get('username'))
        real_data = self.request.data
        real_data.update({'ad': self.kwargs.get('pk')})
        real_data.update({'direction': direction})
        real_data.update({'sender_name': sender_name})
        serializer = self.get_serializer(data=real_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
