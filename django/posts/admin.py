from django.contrib import admin

from posts.models import (
    Comment,
    Group,
    Post,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at', 'author', 'group')
    list_display_links = ('id', 'text', 'created_at', 'author')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created_at',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'author', 'post', 'text')
