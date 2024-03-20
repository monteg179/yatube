import csv
import os
from typing import (
    Any,
    Self,
)

from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
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


class CustomUserManager(UserManager['CustomUser']):

    def load_from_csv(self, file_name: str) -> str:
        if not os.path.exists(file_name):
            return
        with open(file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get('password'):
                    row['password'] = ''
                self.create_user(**row)

    def save_to_csv(self, file_name: str) -> str:
        data = [
            instance.to_dict()
            for instance in self.filter(is_superuser=False)
        ]
        if not data:
            return
        with open(file_name, mode='w') as file:
            writer = csv.DictWriter(file, data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def clear(self) -> str:
        self.filter(is_superuser=False).delete()


class CustomUser(AbstractUser):

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )

    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='self',
        through='Subscription',
        symmetrical=False
    )

    manager = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'<User {self.username}>'

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="users:profile",
            kwargs={'username': self.username}
        )

    def get_full_name(self) -> str:
        return super().get_full_name() or self.username

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_joined': self.date_joined,
            'last_login': self.last_login,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
        }


class Subscription(models.Model):

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    author = models.ForeignKey(
        verbose_name='Автор',
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )

    manager = CustomManager[Self]()

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription',
            ),
        ]
        ordering = ('id',)

    def __str__(self) -> str:
        user = self.user.username
        author = self.author.username
        return f'<Subscription user {user} - author {author}>'

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user.id,
            'author_id': self.author.id,
        }
