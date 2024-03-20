from typing import (
    Any
)
from urllib.parse import (
    urlencode,
)

from django.core.paginator import (
    Page,
)
from django.db.models import (
    QuerySet,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import (
    reverse,
)
from django.views import (
    View,
)

from core.pagination import (
    Paginator,
)


class CustomViewError(Exception):
    pass


class CustomViewRedirect(CustomViewError):

    def __init__(self, path: str, **kwargs) -> None:
        self.url = f'{path}?{urlencode(kwargs)}'


class CustomView(View):

    LOGIN_REQUIRED = False
    LOGIN_URL = 'users:signin'

    async def asetup(self) -> None:
        self.user = await self.request.auser()

    async def authorization(self) -> None:
        if self.LOGIN_REQUIRED and self.user.is_anonymous:
            raise CustomViewRedirect(
                path=reverse(self.LOGIN_URL),
                next=self.request.path
            )

    async def dispatch(
            self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            await self.asetup()
            await self.authorization()
        except CustomViewRedirect as error:
            return redirect(error.url)
        return await super().dispatch(request, *args, **kwargs)


class PaginationMixin:

    PAGINATE_BY = None
    PAGE_KWARG = 'page'

    def paginate_queryset(self) -> QuerySet:
        raise NotImplementedError()

    async def get_page_obj(self) -> Page:
        number = self.request.GET.get(self.PAGE_KWARG)
        if self.PAGINATE_BY:
            paginator = Paginator(
                queryset=self.paginate_queryset(),
                per_page=self.PAGINATE_BY
            )
        else:
            paginator = Paginator(self.paginate_queryset())
        return await paginator.get_page(number)


class TemplateResponseMixin:

    TEMPLATE_NAME = None

    async def template_context(self) -> dict[str, Any]:
        raise NotImplementedError()

    async def template_response(self) -> HttpResponse:
        context = await self.template_context()
        return render(self.request, self.TEMPLATE_NAME, context)


class PostsListView(TemplateResponseMixin, PaginationMixin, CustomView):

    async def get(self, *args, **kwargs) -> HttpResponse:
        return await self.template_response()
