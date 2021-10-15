from django.contrib.auth.models import User
from django.db import models


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    enter = models.DateTimeField(null=False)
    exit = models.DateTimeField(null=False)
    is_active = models.BooleanField()
