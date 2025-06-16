from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow
from django.contrib.auth import get_user_model


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']
        read_only_fields = ['id', 'title', 'slug', 'description']


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        read_only_fields = ['id', 'author', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created', 'post']
        read_only_fields = ['id', 'author', 'created', 'post']


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return value
