from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class DeskUserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('desk_user', 'Desk User'),
        ('manager', 'Manager'),
        ('cleaner', 'Cleaner'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='desk_user')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=20)
    height_cm = models.IntegerField(default=175)
    current_selected_desk_mac_address = models.CharField(max_length=50, default="cd:fb:1a:53:fb:e6")

    height1_cm = models.IntegerField(default=100)
    height1_name = models.CharField(max_length=50, default="Default")
    height2_cm = models.IntegerField(default=100)
    height2_name = models.CharField(max_length=50, default="Default")
    height3_cm = models.IntegerField(default=100)
    height3_name = models.CharField(max_length=50, default="Default")
    height4_cm = models.IntegerField(default=100)
    height4_name = models.CharField(max_length=50, default="Default")
    height5_cm = models.IntegerField(default=100)
    height5_name = models.CharField(max_length=50, default="Default")
    height6_cm = models.IntegerField(default=100)
    height6_name = models.CharField(max_length=50, default="Default")

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        desk_user_profile = DeskUserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


