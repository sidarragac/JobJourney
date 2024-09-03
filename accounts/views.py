from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            """ if user.isCompany:
                companyName = request.POST.get('companyName')
                Company.objects.create(user=user, companyName=companyName)
            else:
                dateOfBirth = request.POST.get('dateOfBirth')
                Person.objects.create(user=user, dateOfBirth=dateOfBirth) """
            return redirect('login')
        print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})