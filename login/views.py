from login.models import CustomUser
from login.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def _is_creator(username, request):
    return username == str(request.user)


class UsersList(APIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
            serializer.save(owner=request.user)
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
            serializer.save(owner=self.request.user)
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
