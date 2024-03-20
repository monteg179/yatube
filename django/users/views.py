from typing import (
    Any,
)

from django.contrib.auth import (
    views,
)
from django.db.models import (
    QuerySet,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import (
    aget_object_or_404,
    redirect,
)
from django.urls import (
    reverse_lazy,
)
from django.views import (
    View,
)
from django.views.generic import (
    CreateView,
)

from core.views import (
    PostsListView,
)
from users.forms import (
    CreationForm,
)
from users.models import (
    CustomUser,
    Subscription,
)


class SignupView(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')


class SigninView(views.LoginView):
    template_name = 'users/signin.html'


class SignoutView(views.LogoutView):
    template_name = 'users/signout.html'


class ProfileView(PostsListView):

    TEMPLATE_NAME = 'users/profile.html'

    def paginate_queryset(self) -> QuerySet:
        return self.author.posts.select_related(
            'group'
        ).only(
            'text', 'created_at', 'group__slug', 'group__title'
        )

    async def asetup(self) -> None:
        await super().asetup()
        self.author = await aget_object_or_404(
            klass=CustomUser,
            username=self.kwargs['username']
        )

    async def template_context(self) -> dict[str, Any]:
        page_obj = await self.get_page_obj()
        if self.user.is_authenticated:
            following = await Subscription.manager.filter(
                user_id=self.user.id, author_id=self.author.id
            ).aexists()
        else:
            following = False
        return {
            'user': self.user,
            'author': self.author,
            'page_obj': page_obj,
            'following': following,
        }


class FollowView(View):

    async def get(self, request: HttpRequest, username: str) -> HttpResponse:
        user = await request.auser()
        author = await aget_object_or_404(CustomUser, username=username)
        if user.username != username:
            await Subscription.manager.aget_or_create(
                user_id=user.id,
                author_id=author.id
            )
        return redirect(author.get_absolute_url())


class UnfollowView(View):

    async def get(self, request: HttpRequest, username: str) -> HttpResponse:
        user = await request.auser()
        author = await aget_object_or_404(CustomUser, username=username)
        await Subscription.manager.filter(
            user_id=user.id, author_id=author.id
        ).adelete()
        return redirect(author.get_absolute_url())
