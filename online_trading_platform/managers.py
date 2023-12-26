from typing import Any
from typing import Optional

from django.contrib.auth.models import BaseUserManager


class EmployeeManager(BaseUserManager):
    def create_user(
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        if not username:
            raise ValueError("The Username field must be set")
        employee = self.model(username=username, **extra_fields)
        employee.set_password(password)
        employee.save()
        return employee

    def create_superuser(
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, password, **extra_fields)
