import datetime

from rest_framework import serializers
from .models import Posts


class PostsSerialiser(serializers.ModelSerializer):
    created = serializers.DateTimeField(required=False)
    author = serializers.ReadOnlyField(source='author.username')

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




