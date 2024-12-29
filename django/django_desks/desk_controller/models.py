from django.db import models

class Desk(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    name = models.CharField(max_length=500)
    state = models.IntegerField(default=1000)
    status = models.CharField(max_length=500, default="Normal")
    #state_data = models.JSONField(default=dict)
    #id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Desk {self.mac_address} - {self.name}"