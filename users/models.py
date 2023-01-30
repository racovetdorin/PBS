from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


class User(AbstractUser):
    first_name = models.CharField(verbose_name='First name', max_length=150, blank=True, default='')
    last_name = models.CharField(verbose_name='Last name', max_length=150, blank=True, default='')
    email = models.EmailField(verbose_name='Email', unique=True, blank=False, null=False)
    objects = UserManager()

    def __str__(self):
        return self.display_full_name()

    def display_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email
