import datetime

from django.contrib.auth.models import User
from rest_framework import serializers, permissions
from .models import Posts


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, max_length=254)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']


class PostsPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Posts):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_superuser


class PostsSerialiser(serializers.ModelSerializer):
    created = serializers.DateTimeField(required=False)
    author = UsersSerializer()

    class Meta:
        model = Posts
        fields = ['title', 'content', 'created', 'author']
        read_only_fields = ['author', 'created']

    def create(self, validated_data):
        return Posts.objects.create(**validated_data)

    def update(self, instance: Posts, validated_data):
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance





