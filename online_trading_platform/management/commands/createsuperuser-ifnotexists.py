from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from config_data import dirs
from config_data.config import load_config

User = get_user_model()

conf = load_config(str(dirs.DIR_REPO / ".env"))


class Command(BaseCommand):
    """
    Create a superuser if none exist.
    Takes args from environment variables.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        username = conf.django.superuser_username
        password = conf.django.superuser_password
        email = conf.django.superuser_email

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User '{username}' exists already")
            return

        User.objects.create_superuser(
            username=username, password=password, email=email
        )

        self.stdout.write(f"Superuser '{username}' was created successfully")
        return
