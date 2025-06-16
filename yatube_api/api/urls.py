from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router_v1 = routers.DefaultRouter()

router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'posts/(?P<post_id>[\d]+)/comments',
                   CommentViewSet, basename='comment')
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
