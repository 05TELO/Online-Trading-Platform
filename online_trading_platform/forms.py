from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import Employee


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Employee
        fields = (
            "username",
            "merchant",
            "position",
        )


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = (
            "username",
            "merchant",
            "position",
        )
