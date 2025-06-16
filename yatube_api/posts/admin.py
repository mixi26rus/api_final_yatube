from django.contrib import admin
from .models import Group, Post, Comment, Follow


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'pub_date', 'author', 'group', 'image')
    search_fields = ('text', 'author__username', 'group__title')
    list_filter = ('pub_date', 'author', 'group')
    readonly_fields = ('pub_date',)
    list_editable = ('group',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created', 'author', 'post')
    search_fields = ('text', 'author__username', 'post__text')
    list_filter = ('created', 'author', 'post')
    readonly_fields = ('created',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')
    search_fields = ('user__username', 'following__username')
    list_filter = ('user', 'following')
