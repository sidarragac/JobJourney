from django.db import models
from accounts.models import User

# Create your models here.
class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class RoadMap(models.Model):
    mainGoal = models.CharField(max_length=100)
    content = models.JSONField()
    completionPercentage = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    idInterest = models.ForeignKey(Interest, on_delete=models.CASCADE)

class Checkpoint(models.Model):
    step = models.CharField(max_length=100)
    checked = models.BooleanField()
    idRoadMap = models.BooleanField()