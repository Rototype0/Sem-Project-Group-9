from django.db import models

class Desk(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    name = models.CharField(max_length=500)
    state_data = models.JSONField(default=list)


    def __str__(self):
        return f"Desk {self.mac_address} - {self.name}"