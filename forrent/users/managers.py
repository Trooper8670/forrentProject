from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, phone=None,
                     password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            if not email and not phone:
                raise ValueError('The given email/phone must be set')

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(
                email=email,
                **extra_fields
            )

        if phone:
            if not username:
                username = phone

            user = self.model(
                username=username,
                phone=phone,
                **extra_fields
            )

        # проверяем является ли пользователь
        # суперпользователем
        #
        if extra_fields.get('is_staff'):
            user = self.model(
                email=email,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )
