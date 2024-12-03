from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class DeskUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=20)
    height = models.IntegerField(default=175)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        desk_user_profile = DeskUserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


