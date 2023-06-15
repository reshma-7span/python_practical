from rest_framework import serializers
from .models import User, Post, Like


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['name', 'email',
                  'password']
        extra_kwargs = {
            'password': {'write_only': True},

        }

    def create(self, validate_data):
        # print(validate_data)
        return User.objects.create(**validate_data)


# Registration Serializer Code End #

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'title', 'description', 'content', 'created_at', 'like_count']
        extra_kwargs = {
            'like_count': {'required': False},

        }

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['like_id', 'post', 'user']