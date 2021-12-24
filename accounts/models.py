from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    avatar = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'users'


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance')
    enter = models.DateTimeField(null=True)
    exit = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Enter: {self.enter} Exit: {self.exit}"
