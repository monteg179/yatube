from django.contrib import (
    admin,
)
from django.urls import (
    include,
    path,
)

urlpatterns = [
    path(
        route='admin/',
        view=admin.site.urls
    ),
    path(
        route='about/',
        view=include('about.urls', namespace='about')
    ),
    path(
        route='users/',
        view=include('users.urls', namespace='users')
    ),
    path(
        route='',
        view=include('posts.urls', namespace='posts')
    ),
]
