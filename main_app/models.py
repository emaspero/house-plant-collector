from django.db import models
from django.urls import reverse
from datetime import date

# Tuples here.
TOXICITY = (
    ('Y', 'Yes'),
    ('N', 'No')
)

TIMESOFDAY = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    light = models.CharField(max_length=100)
    water = models.CharField(max_length=100)
    toxic = models.CharField(max_length=1, choices=TOXICITY, default=TOXICITY[0][0])
    description = models.TextField(max_length=500)
    indexPicture = models.URLField(max_length=1000, null=True)
    detailPicture = models.URLField(max_length=1000, null=True)

    def get_absolute_url(self):
        return reverse('plantsDetail', kwargs = {'plant_id': self.id})

    def __str__(self):
        return self.name

    def watered_today(self):
        return self.watering_set.filter(date=date.today()).count() 

class Watering(models.Model):
    date = models.DateField('Watering Date')
    timeOfDay = models.CharField(max_length=1, choices=TIMESOFDAY, default=TIMESOFDAY[0][0])
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Watered in the {self.get_timeOfDay_display()} on {self.date}"

    class Meta:
        ordering = ['-date']