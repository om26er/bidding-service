from rest_framework import serializers

from login.models import CustomUser, ProductAd
from accounts.settings import MEDIA_LOCATION, STATIC_URL


# def _save_avatar_image_if_attached(validated_data):
#     photo_object = validated_data.get('photo')
#     if photo_object:
#         output_path = MEDIA_LOCATION + photo_object.name
#         destination = open(output_path, 'wb+')
#         for chunk in photo_object.chunks():
#             destination.write(chunk)
#         destination.close()
#         return output_path
#     return ''
#
#
# def _save_avatar_image_if_attached(validated_data):
#     photo_object = validated_data.get('photo')
#     if photo_object:
#         output_path = STATIC_URL + photo_object.name
#         destination = open(output_path, 'wb+')
#         for chunk in photo_object.chunks():
#             destination.write(chunk)
#         destination.close()
#         return output_path
#     return ''


class UserSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(required=False)
    email = serializers.EmailField(required=True)
    interests = serializers.CharField(required=False)
    push_notifications_key = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'address', 'phone_number',
                  'city', 'photo', 'interests', 'push_notifications_key')

    def create(self, validated_data):
        data = CustomUser.objects.create(**validated_data)
        data.set_password(validated_data.get('password'))
        return data
        # photo_path = _save_avatar_image_if_attached(validated_data)
        # user = CustomUser.objects.create_user(
        #     username=validated_data.get('username'),
        #     email=validated_data.get('email'),
        # )
        # user.set_password(validated_data.get('password'))
        # user.address = validated_data.get('address')
        # user.city = validated_data.get('city')
        # user.phone_number = validated_data.get('phone_number')
        # user.photo = photo_path
        # user.save()
        # return user


class UserInterestsSerializer(serializers.Serializer):

    interests = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.interests = validated_data.get('interests')
        instance.save()
        return instance


class UserPushIdSerializer(serializers.Serializer):

    push_key = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.push_key = validated_data.get('push_key')
        instance.save()
        return instance


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
