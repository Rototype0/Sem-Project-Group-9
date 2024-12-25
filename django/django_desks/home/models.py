from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('mamanger', 'Manager'),
        ('user', 'User'),
        ('cleaner', 'Cleaner')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role= models.CharField(max_length=20, choices=ROLE_CHOICES)


    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
# Create your models here.
