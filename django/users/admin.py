from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin,
)

from users.models import (
    CustomUser,
    Subscription,
)
from users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
