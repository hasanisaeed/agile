from django.contrib.auth.models import User
from django.db import models


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    enter = models.DateTimeField(null=True)
    exit = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Enter: {self.enter} Exit: {self.exit}"
