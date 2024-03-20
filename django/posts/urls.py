from django.urls import (
    path,
)

from posts import (
    views,
)

app_name = 'posts'

urlpatterns = [
    path(
        route='',
        view=views.IndexView.as_view(),
        name='index',
    ),
    path(
        route='follow/',
        view=views.FollowIndexView.as_view(),
        name='follow_index'
    ),
    path(
        route='group/<slug:slug>/',
        view=views.GroupPostsView.as_view(),
        name='group_list',
    ),
    path(
        route='create/',
        view=views.PostCreateView.as_view(),
        name='post_create',
    ),
    path(
        route='posts/<int:post_id>/edit/',
        view=views.PostUpdateView.as_view(),
        name='post_edit',
    ),
    path(
        route='posts/<int:post_id>/',
        view=views.PostDetailView.as_view(),
        name='post_detail',
    ),
]
