from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from posts.models import Post, Comment, Group, Follow
from .serializers import (PostSerializer, CommentSerializer, 
                          GroupSerializer, FollowSerializer)
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedForFollow


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny] # Могу и IsAuthorOrReadOnly юзать
    pagination_class = None


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedForFollow]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
