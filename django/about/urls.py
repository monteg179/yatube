from django.urls import path

from about import views

app_name = 'about'

urlpatterns = [
    path(
        route='author/',
        view=views.Author.as_view(),
        name='author',
    ),
    path(
        route='tech/',
        view=views.Tech.as_view(),
        name='tech',
    ),
]
