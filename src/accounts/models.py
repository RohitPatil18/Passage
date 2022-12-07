from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers import UserManager


class UserTypeChoice(models.IntegerChoices):
    COMPANY_USER = 1, 'CompanyUser'


class Company(models.Model):
    """
    Database model for entity `Company`
    """
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'company'
        verbose_name_plural = 'Companies'
        default_permissions = ()

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
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
        choices=UserTypeChoice.choices,
        default=UserTypeChoice.COMPANY_USER
    )
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'

    class Meta:
        db_table = 'user'
        default_permissions = ()

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CompanyUser(models.Model):
    """
    Database model for entity `CompanyUser`.
    This entity stores the mapping between company and user
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_users'
        default_permissions = ()

    def __str__(self):
        return f'{self.company.name} <> {self.user}'
