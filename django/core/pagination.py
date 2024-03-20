import math

from django.core.paginator import (
    EmptyPage,
    Page,
    PageNotAnInteger,
)
from django.db.models import (
    QuerySet,
)


class Paginator:

    PER_PAGE_DEFAULT = 10

    def __init__(
        self,
        queryset: QuerySet,
        per_page: int = PER_PAGE_DEFAULT,
        orphans: int = 0,
        allow_empty_first_page: bool = True
    ) -> None:
        self._queryset = queryset
        self._per_page = per_page
        self._orphans = orphans
        self._allow_empty_first_page = allow_empty_first_page
        self._amount = 0
        self._init_amount = False

    async def __aiter__(self):
        for page_number in self.page_range:
            yield await self.page(page_number)

    def validate_number(self, number) -> int:
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            print(f'number = {number}, num_pages = {self.num_pages}')
            raise EmptyPage('That page contains no results')
        return number

    async def acount(self) -> None:
        if self._init_amount:
            return
        self._amount = await self._queryset.acount()
        self._init_amount = True

    async def get_page(self, number) -> Page:
        await self.acount()
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return await self.page(number)

    async def page(self, number) -> Page:
        await self.acount()
        number = self.validate_number(number)
        first = (number - 1) * self.per_page
        last = first + self.per_page
        if last + self._orphans >= self._amount:
            last = self._amount
        data = [item async for item in self._queryset[first:last].aiterator()]
        return Page(data, number, self)

    @property
    def per_page(self) -> int:
        return self._per_page

    @property
    def count(self) -> int:
        return self._amount

    @property
    def num_pages(self) -> int:
        if self.count == 0 and not self._allow_empty_first_page:
            return 0
        hits = max(1, self._amount - self._orphans)
        return math.ceil(hits / self.per_page)

    @property
    def page_range(self) -> range:
        return range(1, self.num_pages + 1)
