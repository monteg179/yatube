from django import (
    template,
)
from django.contrib.auth import (
    get_user_model,
)

User = get_user_model()

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def author_name(author: User) -> str:
    return author.get_full_name()


@register.filter
def author_full_name(author: User) -> str:
    return f'{author.get_full_name()} {author.username}'
