from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('desk_user', 'Desk User'),
        ('manager', 'Manager'),
        ('cleaner', 'Cleaner'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='desk_user')
    age = models.IntegerField(default=20, null=True, blank=True)
    height = models.IntegerField(default=175, null=True, blank=True)

class DeskUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    age = models.IntegerField(default=20)
    height = models.IntegerField(default=175)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created'] and kwargs['instance'].user_type == 'desk_user':
        DeskUserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=CustomUser) 
