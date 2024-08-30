from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    city = models.CharField(max_length=100)
    typeOfUser = models.enums('person', 'company')

    def __str__(self):
        return self.username

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField()

    def __str__(self):
        return self.user.username

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=100)

    def __str__(self):
        return self.companyName