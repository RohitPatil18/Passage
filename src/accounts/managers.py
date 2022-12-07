from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        email_address = kwargs.get('email_address')
        if not email_address:
            raise ValueError('Users must have an email address')

        password = kwargs.get('password')
        if not email_address:
            raise ValueError('Users must have a password')

        user = self.model(
            email_address=self.normalize_email(email_address),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email_address=email_address,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.create_user(**kwargs)
