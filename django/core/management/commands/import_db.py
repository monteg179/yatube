import os

from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from django.db import (
    transaction,
)

from posts.models import (
    Comment,
    Group,
    Post,
)
from users.models import (
    CustomUser,
    Subscription,
)


class Command(BaseCommand):

    help = 'Loads data from csv files'

    USERS = '{}/users.csv'
    SUBSCRIPTIONS = '{}/subscriptions.csv'
    GROUPS = '{}/groups.csv'
    POSTS = '{}/posts.csv'
    COMMENTS = '{}/comments.csv'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('path')

    def handle(self, *args, **kwargs) -> None:
        path = kwargs.get('path')
        if not os.path.isdir(path):
            raise CommandError(f'No such directory: `{path}`')
        with transaction.atomic():
            try:
                CustomUser.manager.load_from_csv(Command.USERS.format(path))
                Subscription.manager.load_from_csv(
                    file_name=Command.SUBSCRIPTIONS.format(path)
                )
                Group.manager.load_from_csv(Command.GROUPS.format(path))
                Post.manager.load_from_csv(Command.POSTS.format(path))
                Comment.manager.load_from_csv(Command.COMMENTS.format(path))
            except Exception as error:
                raise CommandError(error)
