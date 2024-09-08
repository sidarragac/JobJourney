from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    city = models.CharField(max_length=100)
    isCompany = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #First name and last name is associated with the USER class.
    dateOfBirth = models.DateField()

    def __str__(self):
        return self.user.username

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    companyName = models.CharField(max_length=100)

    def __str__(self):
        return self.companyName
    
class SocialMedia(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserSocialMedia(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idSocialMedia = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.idUser