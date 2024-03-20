import os

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from users.models import (
    CustomUser,
)

from dotenv import (
    load_dotenv,
)

load_dotenv()


class Command(BaseCommand):

    help = 'Create superuser'

    def handle(self, *args, **kwargs) -> None:
        try:
            username = os.getenv(key='DJANGO_SUPERUSER_USERNAME')
            email = os.getenv(key='DJANGO_SUPERUSER_EMAIL')
            password = os.getenv(key='DJANGO_SUPERUSER_PASSWORD')
            if username and password and email:
                CustomUser.manager.create_superuser(username, email, password)
        except Exception as error:
            raise CommandError(error)
