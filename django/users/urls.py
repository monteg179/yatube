from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path(
        route='signin/',
        view=views.SigninView.as_view(),
        name='signin',
    ),
    path(
        route='signout/',
        view=views.SignoutView.as_view(),
        name='signout',
    ),
    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup',
    ),
    path(
        route='profile/<str:username>/',
        view=views.ProfileView.as_view(),
        name='profile',
    ),
    path(
        route='profile/<str:username>/follow/',
        view=views.FollowView.as_view(),
        name='profile_follow'
    ),
    path(
        route='profile/<str:username>/unfollow/',
        view=views.UnfollowView.as_view(),
        name='profile_unfollow'
    ),
]
