import os

from django.core.management.base import (
    CommandError,
    CommandParser,
    BaseCommand,
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

    help = 'Save data to csv files'

    USERS = '{}/users.csv'
    SUBSCIPTIONS = '{}/sunscriptions.csv'
    GROUPS = '{}/groups.csv'
    POSTS = '{}/posts.csv'
    COMMENTS = '{}/comments.csv'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('path')

    def handle(self, *args, **kwargs) -> None:
        path = kwargs.get('path')
        if not os.path.isdir(path):
            raise CommandError(f'No such directory: `{path}`')
        try:
            CustomUser.manager.save_to_csv(Command.USERS.format(path))
            Subscription.manager.save_to_csv(
                file_name=Command.SUBSCIPTIONS.format(path)
            )
            Group.manager.save_to_csv(Command.GROUPS.format(path))
            Post.manager.save_to_csv(Command.POSTS.format(path))
            Comment.manager.save_to_csv(Command.COMMENTS.format(path))
        except Exception as error:
            raise CommandError(error)
