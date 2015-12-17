import os

from rest_framework import serializers

from login.models import CustomUser
from accounts.settings import MEDIA_ROOT


def _save_avatar_image_if_attached(validated_data):
    photo_object = validated_data.get('photo')
    if photo_object:
        output_path = os.path.join(MEDIA_ROOT, photo_object.name)
        destination = open(output_path, 'wb+')
        for chunk in photo_object.chunks():
            destination.write(chunk)
        destination.close()
        return output_path
    return ''


class UserSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'address', 'phone_number',
                  'city', 'photo')

    def create(self, validated_data):
        photo_path = _save_avatar_image_if_attached(validated_data)
        user = CustomUser.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.address = validated_data.get('address')
        user.city = validated_data.get('city')
        user.phone_number = validated_data.get('phone_number')
        user.photo = photo_path
        user.save()
        return user

