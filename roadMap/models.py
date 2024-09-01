from django.db import models
from accounts.models import Person

# Create your models here.
class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Roadmap(models.Model):
    mainGoal = models.CharField(max_length=100)
    content = models.JSONField()
    completionPercentage = models.IntegerField()
    username = models.ForeignKey(Person, on_delete=models.CASCADE)
    idInterest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return self.mainGoal

class Checkpoint(models.Model):
    step = models.CharField(max_length=100)
    checked = models.BooleanField()
    idRoadmap = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return self.step