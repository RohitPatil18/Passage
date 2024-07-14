from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager
from authmod.models import RolePermissionsMixin
from core.models import BaseModel


class UserTypeChoice(models.IntegerChoices):
    COMPANY_USER = 1, "CompanyUser"
    VENDOR_USER = 2, "VendorUser"


class User(AbstractBaseUser, RolePermissionsMixin, BaseModel):
    """
    Custom database model for entity `User` which extends
    Django's inbuilt `AbstractBaseUser`
    """

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email_address = models.EmailField(
        max_length=255,
        unique=True,
    )
    user_type = models.IntegerField(
        choices=UserTypeChoice.choices, default=UserTypeChoice.COMPANY_USER
    )
    is_active = models.BooleanField(default=True)
    _is_staff = models.BooleanField(
        _("staff status"),
        db_column="is_staff",
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email_address"

    class Meta:
        db_table = "user"
        default_permissions = ()

    @property
    def is_staff(self):
        return self.is_superuser or self._is_staff

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "password_reset_code"
        default_permissions = ()
