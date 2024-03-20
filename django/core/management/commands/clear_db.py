from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import (
    transaction,
)

from posts.models import (
    Group,
    Post,
    Comment,
)
from users.models import (
    CustomUser,
    Subscription,
)


class Command(BaseCommand):

    help = 'Clear database'

    def handle(self, *args, **kwargs) -> None:
        with transaction.atomic():
            try:
                Comment.manager.clear()
                Post.manager.clear()
                Group.manager.clear()
                Subscription.manager.clear()
                CustomUser.manager.clear()
            except Exception as error:
                raise CommandError(error)
