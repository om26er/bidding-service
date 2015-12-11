from rest_framework import serializers

from login.models import CustomUser, DummyModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'address', 'phone_number',
                  'city')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.address = validated_data.get('address')
        user.city = validated_data.get('city')
        user.phone_number = validated_data.get('phone_number')
        user.save()
        return user


class DummySerializer(serializers.ModelSerializer):

    class Meta:
        model = DummyModel
        fields = ('school',)
