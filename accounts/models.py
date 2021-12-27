from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    avatar = models.CharField(max_length=300, null=True, blank=True)
    # Every users has it's own color
    color = models.CharField(max_length=9, null=False, blank=False)

    class Meta:
        db_table = 'users'


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='attendance')
    enter = models.DateTimeField(null=True)
    exit = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Enter: {self.enter} Exit: {self.exit}"

    class Meta:
        db_table = 'attendance'


class Sprint(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    total = models.IntegerField(default=0)

    class Meta:
        db_table = 'sprint'


class StoryPoint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='points')
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    date = models.DateTimeField()

    # Story Point(S.P) value
    sp = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'story_point'
        unique_together = ['user', 'date']
