from django.db import models
from accounts.models import Person, User
import numpy as np

def genDefaultArray():
    return np.random.rand(1536).tobytes()

class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#000000") # Hexadecimal color code to be shown in charts.

    def __str__(self):
        return self.name
    
class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is interested in {self.interest}'

class Roadmap(models.Model):
    mainGoal = models.TextField()
    content = models.JSONField()
    completionPercentage = models.IntegerField(default=0)
    numberOfLikes = models.IntegerField(default=0)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    embedding = models.BinaryField(default=genDefaultArray())

    def __str__(self):
        return self.mainGoal

class Checkpoint(models.Model):
    numberOfCheckpoint = models.IntegerField(default=0)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, default=0)
    completed = models.BooleanField()

    def __str__(self):
        return f'# Checkpoint: {self.numberOfCheckpoint} - Roadmap ID {self.roadmap}'
    
class LikeRoadmap(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.roadmap}'