import os

from rest_framework import serializers

from login.models import CustomUser, ProductAd
from accounts.settings import MEDIA_ROOT, MEDIA_URL


def _save_avatar_image_if_attached(validated_data):
    photo_object = validated_data.get('photo')
    upload_path = MEDIA_URL+MEDIA_ROOT
    print(upload_path)
    if photo_object:
        output_path = os.path.join(upload_path, photo_object.name)
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


class AdSerializer(serializers.ModelSerializer):

    photo2 = serializers.ImageField(required=False)
    photo3 = serializers.ImageField(required=False)
    photo4 = serializers.ImageField(required=False)
    photo5 = serializers.ImageField(required=False)
    photo6 = serializers.ImageField(required=False)
    photo7 = serializers.ImageField(required=False)
    photo8 = serializers.ImageField(required=False)

    class Meta:
        model = ProductAd
        fields = ('id', 'created', 'title', 'description', 'category', 'price',
                  'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6',
                  'photo7', 'photo8')
