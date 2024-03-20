from typing import (
    Any,
)

from django.contrib.auth import (
    get_user_model,
)
from django.db.models import (
    Count,
    QuerySet,
)
from django.http import (
    HttpResponse,
)
from django.shortcuts import (
    aget_object_or_404,
    redirect,
)

from core.views import (
    CustomView,
    CustomViewRedirect,
    PostsListView,
    TemplateResponseMixin,
)
from posts.forms import (
    PostForm,
    CommentForm,
)
from posts.models import (
    Comment,
    Group,
    Post,
)

User = get_user_model()


class IndexView(PostsListView):

    TEMPLATE_NAME = 'posts/index.html'

    def paginate_queryset(self) -> QuerySet:
        return Post.manager.select_related(
            'author', 'group'
        ).only(
            'text', 'created_at', 'group__slug', 'group__title',
            'author__username', 'author__first_name', 'author__last_name'
        ).order_by(
            '-created_at'
        )

    async def template_context(self) -> dict[str, Any]:
        page_obj = await self.get_page_obj()
        return {
            'user': self.user,
            'page_obj': page_obj,
        }


class FollowIndexView(IndexView):

    LOGIN_REQUIRED = True

    def paginate_queryset(self) -> QuerySet:
        return Post.manager.select_related(
            'group', 'author'
        ).filter(
            author__following__user_id=self.user.id
        ).only(
            'text', 'created_at', 'group__slug', 'group__title',
            'author__username', 'author__first_name', 'author__last_name'
        ).order_by(
            '-created_at'
        )


class GroupPostsView(PostsListView):

    TEMPLATE_NAME = 'posts/group_list.html'

    def paginate_queryset(self) -> QuerySet:
        return self.group.posts.select_related(
            'author'
        ).only(
            'text', 'created_at', 'author__username', 'author__first_name',
            'author__last_name'
        ).order_by(
            '-created_at'
        )

    async def asetup(self) -> None:
        await super().asetup()
        self.group = await aget_object_or_404(Group, slug=self.kwargs['slug'])

    async def template_context(self) -> dict[str, Any]:
        page_obj = await self.get_page_obj()
        return {
            'user': self.user,
            'group': self.group,
            'page_obj': page_obj
        }


class PostDetailView(TemplateResponseMixin, CustomView):

    TEMPLATE_NAME = 'posts/post_detail.html'

    async def asetup(self) -> None:
        await super().asetup()
        queryset = Post.manager.select_related(
            'author', 'group'
        ).annotate(
            author_posts_amount=Count('author__posts')
        )
        self.post_obj = await aget_object_or_404(
            klass=queryset,
            id=self.kwargs['post_id']
        )

    async def template_context(self) -> dict[str, Any]:
        queryset = self.post_obj.comments.select_related(
            'author'
        ).only(
            'text', 'author__username'
        )
        comments = [comment async for comment in queryset.aiterator()]
        return {
            'user': self.user,
            'post': self.post_obj,
            'comments': comments,
            'form': self.form,
        }

    async def get(self, *args, **kwargs) -> HttpResponse:
        self.form = CommentForm()
        return await self.template_response()

    async def post(self, *args, **kwargs) -> HttpResponse:
        self.form = CommentForm(data=self.request.POST)
        if self.form.is_valid():
            await Comment.manager.acreate(
                text=self.form.cleaned_data['text'],
                author_id=self.user.id,
                post_id=self.post_obj.id
            )
            return redirect(self.post_obj.get_absolute_url())
        return await self.template_response()


class PostCreateView(TemplateResponseMixin, CustomView):

    LOGIN_REQUIRED = True

    TEMPLATE_NAME = 'posts/create_post.html'

    async def asetup(self) -> None:
        await super().asetup()
        self.groups = [group async for group in Group.manager.aiterator()]

    async def template_context(self) -> dict[str, Any]:
        return {
            'user': self.user,
            'form': self.form,
            'is_edit': False,
        }

    async def get(self, *args, **kwargs) -> HttpResponse:
        self.form = PostForm(self.groups)
        return await self.template_response()

    async def post(self, *args, **kwargs) -> HttpResponse:
        self.form = PostForm(self.groups, data=self.request.POST)
        if self.form.is_valid():
            data = self.form.cleaned_data
            await Post.manager.acreate(
                text=data['text'],
                group_id=data['group'],
                author_id=self.user.id
            )
            return redirect(self.user.get_absolute_url())
        return await self.template_response()


class PostUpdateView(TemplateResponseMixin, CustomView):

    LOGIN_REQUIRED = True

    TEMPLATE_NAME = 'posts/create_post.html'

    async def asetup(self) -> None:
        await super().asetup()
        self.post_obj = await aget_object_or_404(
            klass=Post,
            id=self.kwargs['post_id']
        )
        self.groups = [group async for group in Group.manager.aiterator()]

    async def authorization(self) -> None:
        await super().authorization()
        if not self.post_obj.can_edit(self.user):
            raise CustomViewRedirect(self.post_obj.get_absolute_url())

    async def template_context(self) -> dict[str, Any]:
        return {
            'user': self.user,
            'form': self.form,
            'is_edit': True,
        }

    async def get(self, *args, **kwargs) -> HttpResponse:
        self.form = PostForm(
            groups=self.groups,
            initial={
                'text': self.post_obj.text,
                'group': self.post_obj.group_id
            }
        )
        return await self.template_response()

    async def post(self, *args, **kwargs) -> HttpResponse:
        self.form = PostForm(
            groups=self.groups,
            data=self.request.POST
        )
        if self.form.is_valid():
            data = self.form.cleaned_data
            self.post_obj.text = data['text']
            self.post_obj.group_id = data['group']
            await self.post_obj.asave()
            return redirect(self.user.get_absolute_url())
        return await self.template_response()
