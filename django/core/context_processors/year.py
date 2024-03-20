from django.http import (
    HttpRequest,
)
from django.utils.timezone import (
    now,
)


def year(request: HttpRequest):
    return {
        'year': now().year
    }
