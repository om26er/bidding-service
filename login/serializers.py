from rest_framework import serializers

from login.models import(
    CustomUser,
    ProductAd,
    Comments,
    AdCategories,
)


class UserSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(required=False)
    email = serializers.EmailField(required=True)
    interests = serializers.CharField(required=False)
    push_notifications_key = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'address', 'phone_number',
                  'city', 'photo', 'interests', 'push_notifications_key')


class UserInterestsSerializer(serializers.Serializer):

    interests = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.interests = validated_data.get('interests')
        instance.save()
        return instance


class UserPushIdSerializer(serializers.Serializer):

    push_key = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.push_key = validated_data.get('push_key')
        instance.save()
        return instance


class AdSerializer(serializers.ModelSerializer):

    comments = serializers.StringRelatedField(many=True, required=False)
    currency = serializers.CharField(required=True)

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
                  'photo7', 'photo8', 'comments', 'currency')


class AdCommentSerializer(serializers.Serializer):

    review = serializers.CharField(required=True)
    stars = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        review_text = validated_data.get('review', None)
        stars = validated_data.get('stars', None)
        if review_text and stars:
                comment = Comments(ad=instance,
                                   review=validated_data.get('review'),
                                   stars=validated_data.get('stars'))
                comment.save()
                return comment
        return instance


class AdCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments


class AdCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdCategories
