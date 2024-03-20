from typing import (
    Any,
    Self,
)

from django.contrib.auth import (
    get_user_model,
)
from django.db import (
    models,
)
from django.urls import (
    reverse,
)

from core.models import (
    CustomManager,
)

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Название группы',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание группы',
        blank=True,
    )

    manager = CustomManager[Self]()

    class Meta():
        verbose_name = 'Сообщество постов'
        verbose_name_plural = 'Сообщества постов'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'<Group {self.slug}>'

    def get_absolute_url(self) -> str:
        return reverse(
            viewname='posts:group_list',
            kwargs={
                'slug': self.slug,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
        }


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста'
    )
    author = models.ForeignKey(
        verbose_name='Автор поста',
        to=User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        verbose_name='Группа постов',
        to=Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата последнего изменения',
        auto_now=True
    )

    manager = CustomManager[Self]()

    class Meta():
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-id',)

    def __str__(self) -> str:
        return f'<Post {self.id}>'

    def get_absolute_url(self) -> str:
        return reverse(
            viewname='posts:post_detail',
            kwargs={
                'post_id': self.id,
            }
        )

    def can_edit(self, user) -> bool:
        return self.author_id == user.id

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'text': self.text,
            'author_id': self.author_id,
            'group_id': self.group_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        verbose_name='Автор комментария',
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        verbose_name='Комментируемый пост',
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    manager = CustomManager[Self]()

    class Meta():
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-id',)

    def __str__(self) -> str:
        return f'<Comment {self.id}>'

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'text': self.text,
            'author_id': self.author_id,
            'post_id': self.post_id,
            'created_at': self.created_at,
        }
