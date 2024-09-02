from django.db import models
from accounts.models import Person

class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Roadmap(models.Model):
    mainGoal = models.TextField()
    content = models.JSONField()
    completionPercentage = models.IntegerField(default=0)
    numberOfLikes = models.IntegerField(default=0)
    username = models.ForeignKey(Person, on_delete=models.CASCADE)
    idInterest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return self.mainGoal

class Checkpoint(models.Model):
    numberOfCheckpoint = models.IntegerField(default=0)
    idRoadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    completed = models.BooleanField()

    def __str__(self):
        return f'# Checkpoint: {self.numberOfCheckpoint} - Roadmap ID {self.idRoadmap}'