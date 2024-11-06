from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "city", "isCompany"]

class GoogleRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    city = forms.CharField(max_length=150)
    isCompany = forms.BooleanField(required=False)
    companyName = forms.CharField(max_length=150, required=False)
    dateOfBirth = forms.DateField(required=False)
    image = forms.URLField(required=False)

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            city=self.cleaned_data['city'],
            isCompany=self.cleaned_data['isCompany'],
            image=self.cleaned_data['image'],
        )
        return user