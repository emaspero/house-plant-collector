from django.db import models

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    light = models.CharField(max_length=100)
    water = models.CharField(max_length=100)
    toxic = models.BooleanField()
    description = models.TextField(max_length=500)
    indexPicture = models.URLField(max_length=1000, null=True)
    detailPicture = models.URLField(max_length=1000, null=True)
