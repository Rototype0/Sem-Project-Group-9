from django.db import models

class HeightProfile(models.Model):
    name = models.CharField(max_length = 100)
    height = models.IntegerField()

    def __str__(self):
        return self.name
    
class Desk(models.Model):
    name = models.CharField(max_length = 100)
    height = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

