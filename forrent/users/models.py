from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), null=True, blank=True, max_length=255, )
    last_name = models.CharField(_('last name'), null=True, blank=True, max_length=255)
    email = models.EmailField(_('email address'),
                              blank=True,
                              unique=True,
                              default='user@user.com')
    email_verify = models.BooleanField(default=False)
    phone = PhoneNumberField(blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    is_verified = models.BooleanField(_('verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
