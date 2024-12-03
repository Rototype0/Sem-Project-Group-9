from django.db import models

class Config (models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

class State (models.Model):
    position_mm = models.IntegerField (null=False, blank=False)
    speed_mms = models.IntegerField()
    status = models.CharField(max_length=100) #not sure about this
    isPositionLost = models.BooleanField(default=False)
    isOverloadProtectionUp = models.BooleanField(default=False)
    isOverloadProtectionDown = models.BooleanField(default=False)
    isAntiCollision = models.BooleanField(default=False)


class DeskUser (models.Model):
    username = models.CharField (max_length = 100, null=False, blank=False)
    height = models.IntegerField (null=False, blank=False) #position_mm?
    fav_height_set = models.OneToOneField(
        'FavouritePositionSets', 
        on_delete=models.CASCADE, 
        related_name='user'
    )

class FavouritePositionSets (models.Model):
    pass

class FavPosition (models.Model):
    desk_height = models.IntegerField (null=False, blank=False)
    fav_position_set = models.ForeignKey(
        FavouritePositionSets, 
        on_delete=models.CASCADE, 
        related_name='fav_positions'
    )